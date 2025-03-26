import numpy as np
from scipy.stats import rankdata
from pysmooth import smooth
import pandas as pd
import argparse


def birra(
    data,
    prior=0.05,
    n_bins=50,
    n_iter=10,
    return_all=False,
    cor_stop=1,
    impute_method="random",
):
    """
    Bayesian Inference Rank Rank Aggregation (BIRRA).

    Args:
        data (np.ndarray): 2D numpy array where rows are items (genes) and
                           columns are ranked lists (datasets). Lower values
                           indicate higher ranks (e.g., rank 1 is best).
                           Can contain NaNs if impute_method is specified.
        prior (float): Prior probability of an item being 'positive' (highly ranked).
        n_bins (int): Number of bins to discretise normalised ranks.
        n_iter (int): Number of iterations for the algorithm.
        return_all (bool): If True, return a dict with results, imputed data,
                           and Bayes factors. Otherwise, return only aggregate ranks.
        cor_stop (float or None): Correlation threshold between consecutive
                                  aggregate ranks to stop iteration early.
                                  Set to None to disable early stopping.
        impute_method (str or None): Method for handling NaN values.
                                     'random': Impute NaNs with random ranks
                                               greater than the max observed rank
                                               in that column.
                                     None: Raise ValueError if NaNs are present.

    Returns:
        np.ndarray or dict: Depending on return_all.
                            If return_all is False: 1D array of aggregate ranks.
                            If return_all is True: Dict containing 'result',
                            'data' (imputed), and 'BF'.

    Raises:
        ValueError: If data is not a 2D numpy array.
        ValueError: If data contains NaNs and impute_method is None.
    """
    if not isinstance(data, np.ndarray) or data.ndim != 2:
        raise ValueError("data must be a 2D numpy array")

    n_genes, n_datasets = data.shape

    # --- Imputation Step ---
    if np.isnan(data).any():
        if impute_method is None:
            raise ValueError(
                "Input data contains NaNs, but impute_method is None."
            )
        elif impute_method == "random":
            print("Imputing NaN values using 'random' method...")
            data_imputed = data.copy()
            max_ranks_per_col = np.nanmax(data, axis=0)

            for j in range(n_datasets):
                col_data = data_imputed[:, j]
                nan_mask_col = np.isnan(col_data)
                n_nans_col = np.sum(nan_mask_col)

                if n_nans_col == 0:
                    continue

                max_r = max_ranks_per_col[j]

                if np.isnan(max_r):  # Column was all NaNs
                    low = 1
                    high = n_genes
                    print(
                        f"Warning: Column {j} contains only NaNs. Imputing ranks randomly between {low} and {high}."
                    )
                else:
                    low = int(np.floor(max_r) + 1)
                    high = n_genes

                if low > high:
                    imputed_values = np.full(n_nans_col, high)
                elif low == high:  # Only one possible value to impute
                    imputed_values = np.full(n_nans_col, high)
                else:
                    # Generate random integers in the interval [low, high]
                    imputed_values = np.random.randint(
                        low, high + 1, size=n_nans_col
                    )

                data_imputed[nan_mask_col, j] = imputed_values
            print("Imputation complete.")
            data_proc = data_imputed
        else:
            raise ValueError(f"Unknown impute_method: {impute_method}")
    else:
        if impute_method is not None:
            print("No NaNs found in input data.")
        data_proc = data
    # --- End Imputation Step ---

    prior_or = prior / (1 - prior)
    n_pos = int(np.floor(n_genes * prior))
    # Normalise ranks using the processed data (potentially imputed)
    # Ensure normalisation handles potential ties correctly if ranks aren't contiguous
    # A simple division might not be robust if ranks aren't 1..n_genes.
    # Let's normalise based on the max possible rank n_genes.
    data_normalised = data_proc / n_genes  # Rank / Total possible ranks

    bayes_factors = np.zeros((n_bins, n_datasets))
    # Binning based on normalised ranks
    binned_data = np.ceil(data_normalised * n_bins).astype(int)
    # Ensure bins are within [1, n_bins]
    np.clip(binned_data, 1, n_bins, out=binned_data)

    # Initial aggregation based on mean *normalised* rank
    agg_ranks_norm = np.mean(data_normalised, axis=1)
    # Convert back to rank order (lower mean normalised rank -> better aggregate rank)
    agg_ranks = rankdata(agg_ranks_norm, method="ordinal")

    for iter_num in range(n_iter):
        print(f"Starting iteration {iter_num + 1}/{n_iter}...")
        prev_agg_ranks = agg_ranks.copy()

        # Determine positive/negative set based on current aggregate ranks
        # Use 'min' rank to handle ties in agg_ranks consistently
        ranks_for_mask = rankdata(agg_ranks, method="min")
        pos_mask = ranks_for_mask <= n_pos
        neg_mask = ~pos_mask

        # Compute Bayes factors for each bin and dataset
        for i in range(n_datasets):
            for j in range(1, n_bins + 1):
                # Find genes whose rank in dataset 'i' falls into bin 'j' or lower
                current_bins_mask = binned_data[:, i] <= j
                # Calculate TPR and FPR contributors
                # Summing boolean masks directly counts True values
                tpr_count = np.sum(pos_mask & current_bins_mask)
                fpr_count = np.sum(neg_mask & current_bins_mask)

                # Add-one (Laplace) smoothing to avoid division by 0 or log(0)
                bayes_factors[j - 1, i] = np.log(
                    (tpr_count + 1) / (fpr_count + 1) / prior_or
                )

        # Apply smoothing & reverse cummax to curves for each dataset
        for i in range(n_datasets):
            col = bayes_factors[:, i].copy()
            # Apply 3RS3R smoothing
            smoothed = smooth(
                x=col, kind="3RS3R", twiceit=False, endrule="Tukey"
            )
            # Enforce monotonicity (non-increasing as rank threshold increases)
            # by taking cumulative maximum from the end
            rev_cummax = np.maximum.accumulate(smoothed[::-1])[::-1]
            bayes_factors[:, i] = rev_cummax

        # Down-weight the contribution of the 'best' dataset for each bin
        if n_datasets >= 2:
            for bin_row in range(n_bins):
                row_data = bayes_factors[bin_row, :]
                # Find indices that would sort the row in descending order
                sorted_indices = np.argsort(-row_data)
                # Replace the highest BF with the second highest BF
                first_idx = sorted_indices[0]
                second_idx = sorted_indices[1]
                bayes_factors[bin_row, first_idx] = row_data[second_idx]

        # --- Map binned ranks back to Bayes factors ---
        # Ensure indexing is correct
        # flat_bins contains the bin number (1 to n_bins) for each gene in each dataset (column-major order)
        flat_bins = binned_data.ravel(order="F")
        # dataset_indices repeats 0, 0, ..., 1, 1, ..., n_datasets-1
        dataset_indices = np.repeat(np.arange(n_datasets), n_genes)
        # Select the corresponding Bayes factor using bin number (adjusting for 0-based index)
        # and dataset index
        selected_bf = bayes_factors[flat_bins - 1, dataset_indices]

        # Reshape back to (n_genes, n_datasets)
        bayes_data = selected_bf.reshape(
            n_genes, n_datasets, order="F"
        )  # Use order='F' for column-major fill

        # --- Aggregate Bayes factors and update ranks ---
        # Sum the log Bayes factors across datasets for each gene
        row_sums = np.sum(bayes_data, axis=1)
        # New aggregate ranks: Higher sum means stronger evidence for being 'positive'
        # We rank by descending sum (-row_sums)
        agg_ranks = rankdata(
            -row_sums, method="average"
        )  # Use average for ties in final ranks

        # --- Check for convergence ---
        if cor_stop is not None and not np.isnan(cor_stop) and iter_num > 0:
            # Calculate Pearson correlation between current and previous aggregate ranks
            # Ensure no NaNs in ranks before calculating correlation
            if np.isnan(agg_ranks).any() or np.isnan(prev_agg_ranks).any():
                print(
                    "Warning: NaN detected in aggregate ranks, skipping convergence check for this iteration."
                )
            else:
                # Use rowvar=False because each variable (agg_ranks, prev_agg_ranks) is a column
                cprev = np.corrcoef(agg_ranks, prev_agg_ranks)[0, 1]
                print(
                    f"Iteration {iter_num + 1}: Correlation with previous = {cprev:.6f}"
                )
                # Check if correlation meets the stopping criterion (allowing for float precision)
                if cprev >= cor_stop - 1e-9:  # Looser tolerance
                    print(f"Converged after iteration {iter_num + 1}.")
                    break
        else:
            print(f"Iteration {iter_num + 1} complete.")

    if iter_num == n_iter - 1 and cor_stop is not None:
        print("Warning: Maximum iterations reached without convergence.")

    if return_all:
        return {
            "result": agg_ranks,
            "data": bayes_data,
            "BF": bayes_factors,
            "imputed_input": data_proc,
        }
    else:
        return agg_ranks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run BIRRA rank aggregation with optional NaN imputation."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to CSV file with ranked lists (genes x datasets). Lower rank is better. Use 'NA' or empty string for missing values.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the aggregate ranks CSV file.",
    )
    parser.add_argument(
        "--prior",
        type=float,
        default=0.05,
        help="Prior probability of being highly ranked.",
    )
    parser.add_argument(
        "--n_bins",
        type=int,
        default=50,
        help="Number of bins for rank discretisation.",
    )
    parser.add_argument(
        "--n_iter", type=int, default=10, help="Maximum number of iterations."
    )
    parser.add_argument(
        "--cor_stop",
        type=float,
        default=0.999,
        help="Correlation threshold for early stopping (set high, e.g., 0.999 or 1.0). Use 'nan' or omit for no early stopping.",
    )
    parser.add_argument(
        "--impute",
        type=str,
        default="random",
        choices=["random", "none"],
        help="Imputation method for missing values ('random' or 'none').",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility, especially with imputation.",
    )

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        np.random.seed(args.seed)
        print(f"Using random seed: {args.seed}")

    # Read data, treating common missing value strings as NaN
    ranked_effects = pd.read_csv(args.input, na_values=["NA", "NaN", "N/A", ""])

    data_matrix = ranked_effects.values.astype(
        float
    )  # Ensure float type for NaNs

    # Handle cor_stop argument properly (allow disabling)
    cor_stop_val = args.cor_stop
    # argparse doesn't easily handle None, so we check for a sentinel value like float('nan') or a string
    # Let's refine the command line to accept 'nan' string for disabling cor_stop
    if isinstance(args.cor_stop, str) and args.cor_stop.lower() == "nan":
        cor_stop_val = None
        print("Early stopping disabled.")
    elif args.cor_stop > 1.0 or args.cor_stop < 0.0:
        print(
            f"Warning: cor_stop value {args.cor_stop} is outside [0, 1]. Using default 0.999."
        )
        cor_stop_val = 0.999
    else:
        print(f"Using correlation stop threshold: {cor_stop_val}")

    # Map impute argument 'none' to None
    impute_method_val = args.impute if args.impute != "none" else None

    result = birra(
        data=data_matrix,
        prior=args.prior,
        n_bins=args.n_bins,
        n_iter=args.n_iter,
        return_all=False,
        cor_stop=cor_stop_val,
        impute_method=impute_method_val,
    )

    pd.DataFrame({"aggregate_rank": result}).to_csv(args.output, index=False)
    print(f"Aggregate ranks saved to {args.output}")
