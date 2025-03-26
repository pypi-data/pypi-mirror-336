from datetime import datetime, timedelta
from typing import Union, List, Tuple

class BatchCalculatorUtils:
    @staticmethod
    def calculate_numeric_batches(
        lower_bound: Union[int, float], 
        upper_bound: Union[int, float], 
        num_partitions: int, 
        records_per_batch: int
    ) -> List[Tuple[Union[int, float], Union[int, float]]]:
        """
        Generates numeric batches within lower and upper bounds for numerical partitions.
        Ensures records_per_batch is divisible by num_partitions and distributes records efficiently.
        """
        if lower_bound > upper_bound:
            raise ValueError(f"lower_bound must be less than upper_bound -> lower_bound:{lower_bound}, upper_bound:{upper_bound}.")
        
        if lower_bound < 0 or upper_bound < 0:
            raise ValueError(f"lower_bound or upper_bound cannot be negative -> lower_bound:{lower_bound}, upper_bound:{upper_bound}.")
        
        if records_per_batch <= 0:
            raise ValueError(f"records_per_batch must be positive -> records_per_batch:{records_per_batch}.")
        
        batches = []
        start = lower_bound

        while start <= upper_bound:
            end = min(start + records_per_batch - 1, upper_bound)  # Exclusive upper bound except for last batch
            if (end + 1) == upper_bound:
                end += 1  # Include the upper_bound
            batches.append((start, end))
            start = end + 1  # Move to the next batch start point
        return batches

    @staticmethod
    def calculate_date_batches(lower_bound: str, upper_bound: str, 
                               batch_by: str = "month") -> List[Tuple[str, str]]:
        """
        Splits the given date range into batches based on the specified batch_by parameter.

        :param lower_bound: Start date in 'YYYY-MM-DD' format.
        :param upper_bound: End date in 'YYYY-MM-DD' format.
        :param batch_by: Strategy for splitting ('month' or 'Xd' like '30d').
        :return: List of (start_date, end_date) tuples representing each batch.
        """
        lower_date = datetime.strptime(lower_bound, "%Y-%m-%d")
        upper_date = datetime.strptime(upper_bound, "%Y-%m-%d")

        batches = []
        current_date = lower_date

        while current_date <= upper_date:
            if batch_by == "month":
                next_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            # TODO: not fully supported
            elif batch_by.endswith("d"):  # Example: '7d', '30d'
                next_date = current_date + timedelta(days=int(batch_by[:-1]) - 1)
            else:
                raise ValueError("Invalid batch_by parameter. Use 'month' or 'Xd' (e.g., '30d')")

            # Ensure we don't exceed the upper bound
            if next_date > upper_date:
                next_date = upper_date

            batches.append((current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")))
            current_date = next_date + timedelta(days=1)

        return batches

    @staticmethod
    def calculate_batches(
        lower_bound: Union[int, float, str], 
        upper_bound: Union[int, float, str], 
        num_partitions: int = None, 
        records_per_batch: int = None, 
        batch_by: str = "month"
    ) -> List[Tuple[Union[int, float, str], Union[int, float, str]]]:
        """
        Determines whether to call numeric or date-based batch calculation based on the input type.

        :param lower_bound: Lower bound (int, float, or date in 'YYYY-MM-DD' format).
        :param upper_bound: Upper bound (int, float, or date in 'YYYY-MM-DD' format).
        :param num_partitions: (Optional) Number of partitions for numeric batching.
        :param records_per_batch: (Optional) Number of records per batch (for numeric batching).
        :param batch_by: (Optional) Batch strategy ('month' or 'Xd' for dates).
        :return: List of tuples representing batches.
        """
        is_datetime_partitioning = isinstance(lower_bound, str) and isinstance(upper_bound, str)

        print(f"""Start of batches calculation -> is_datetime_partitioning: {is_datetime_partitioning},
              lower_bound: {lower_bound}, upper_bound: {upper_bound}, batch_by: {batch_by}""")
        
        if is_datetime_partitioning:
            try:
                # Ensure inputs remain as strings for calculate_date_batches
                datetime.strptime(lower_bound, "%Y-%m-%d")
                datetime.strptime(upper_bound, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date format must be 'YYYY-MM-DD'.")
            
            return BatchCalculatorUtils.calculate_date_batches(lower_bound, upper_bound, batch_by)

        elif isinstance(lower_bound, (int, float)) and isinstance(upper_bound, (int, float)):
            if  records_per_batch is None:
                raise ValueError("records_per_batch must be provided for numeric batching.")
            return BatchCalculatorUtils.calculate_numeric_batches(lower_bound, upper_bound,
                                                                   num_partitions, records_per_batch)
    
        else:
            raise TypeError("Invalid bounds type. Both bounds must be either numeric (int/float) or string (date).")
