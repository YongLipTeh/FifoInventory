"""
Fifo
====

Provides
	1. Tracking the ins and outs of inventories
	2. Calculation of Cost of Goods Sold based on First in First Out method
	3. Calculation of Sales Revenue and Gross Profit

How to use the documentation
----------------------------
Documentation is available as docstrings in the code.

You may import this file by using the following import::

	>>> import fifo

"""

from attrs import frozen, field, define, setters
from attrs.validators import instance_of
from typing import ClassVar, Iterator, List, Tuple
import itertools
import datetime as dt
import copy

def date_converter(date: str | dt.date) -> dt.date:
    """
    Convert date into comparable transactions
    through attrs converter during runtime.

    Parameters
    ----------
    date
                    Convert string to date format for easy comparison.
                    Date must be provided in iso format "yyyy-MM-dd"

    Returns
    -------
    datetime.date
                    Ensure that both string and datetime format is allowed
    """
    if isinstance(date, str):
        return dt.date.fromisoformat(date)
    elif isinstance(date, dt.date):
        return date


@define(order=True)
class Purchases:
    """Keeping track of the purchases done, the beginning inventory is named p0, the first object.

    These attributes have the same properties as its child, Sales.\n
    This class is intentionally made to be editable for calculation purpose,
    however it should be treated as a frozen class.

    Attributes
    ----------
    date_iso
                    The date given in iso_format, string or datetime.date are allowed, format: yyyy-MM-dd\n
                    Its purpose is to arrange the transactions in order, the absolute date does not matter.
    classification
                    purchaases or sales, enable distinctions even after the class is imported.
    index
                    A unique index given to all objects, it will be generated automatically.
    index_global
                    To keep track of the indexes of each object created.\n
                    Purchase — batch no.\n
                    Sales — order no.

    """

    date_iso: str | dt.date = field(converter=date_converter, on_setattr=setters.frozen)
    quantity: int = field(validator=instance_of(int))
    unit_price: float = field(
        validator=instance_of(int | float), on_setattr=setters.frozen
    )
    classification: ClassVar[str] = field(
        init=False, default="purchases", on_setattr=setters.frozen
    )
    index: int = field(init=False)
    index_global: ClassVar[Iterator[int]] = itertools.count()

    @quantity.validator
    @unit_price.validator
    def negative_value(self, attribute, value: int):
        if value < 0:
            raise ValueError

    @classmethod
    def _reset_index(cls) -> None:
        cls.index_global = itertools.count()

    @property
    def total_value(self) -> float:
        """Total price of each order"""
        return self.quantity * self.unit_price

    def __attrs_post_init__(self):
        self.index = next(Purchases.index_global)


@define(order=True)
class Sales(Purchases):
    """
    Inherited from Purchases, the only thing different is the classification and index no.

    Purchases' indexes do not mix with Sales' indexes
    """

    classification: ClassVar[str] = field(
        init=False, default="sales", on_setattr=setters.frozen
    )
    index_global: ClassVar[Iterator[int]] = itertools.count()

    def __attrs_post_init__(self):
        self.index = next(Sales.index_global)


class SalesMoreThanInventoryError(Exception):
    """Exception handling. Ensure that all sales are possible, sales cannot occur if inventory has less to provide."""

    pass


@frozen
class Inventory:
    """Enables the calculation of revenues and cost of goods sold.

    Takes in lists of inventory purchases,
    sort it according to date and deduct each sales from the available inventory

    Parameters
    ----------
    purchase_list : list[Purchases]
                    List of all the inventory ins.

    sales_list : list[Sales]
                    List of all the inventory outs

    Notes
    -----
    The beginning purchase is the leftover inventory from last month.

    """

    purchase_list: list[Purchases] = field(
        factory=list, converter=lambda x: [copy.deepcopy(y) for y in x]
    )
    sales_list: list[Sales] = field(
        factory=list, converter=lambda x: [copy.deepcopy(y) for y in x]
    )

    @property
    def purchase_list_sorted(self):
        return sorted(self.purchase_list, key=lambda k: (k.date_iso, k.index))

    @property
    def sales_list_sorted(self):
        return sorted(self.sales_list, key=lambda k: (k.date_iso, k.index))

    @property
    def transaction_list(self):
        return self.purchase_list_sorted + self.sales_list_sorted

    @property
    def sorted_jobs_list(self):
        return sorted(self.transaction_list, key=lambda k: k.date_iso)

    def sales_revenue(self) -> float:
        """The sum of products of all orders."""
        earnings = [x.total_value for x in self.sales_list]
        return sum(earnings)

    def cogs_inventory(
        self,
    ) -> Tuple[List[Purchases], List[Purchases]] | Tuple[List[Purchases], list]:
        """Obtains a list of inventory ins and outs,
        sort them and use first in first out method to deduct sales from inventories.

        Parameters
        ----------
        purchase_list : list[Purchases]
                Inventory ins, need not be sorted.
        sales_list : list[Sales]
                Inventory outs, need not be sorted.

        Same Date Notes
        ---------------
        When purchases and sales happens on the same day, purchases will take precedence by which is added first, and then the sales.\n
        The absolute dates do not actually matter, only the relative dates matter, its only purpose is to tell which transaction came first.

        Returns
        -------
        cogs_list : list[Purchases]
                The list of sales will be updated to list of sales according how they are extracted.
        inventory_list : list[Purchases]
                The leftover inventory at the end of the month.

        Notes
        -----
        These two variables are the most influential parameters in this calculation.\n
        Most bugs can be corrected by inspecting these two variables.

        """

        sorted_jobs_list = copy.deepcopy(self.sorted_jobs_list)

        cogs_list: list[Purchases] = []
        inventory_list: list[Purchases] = []

        def _inventory_is_able_to_be_transfered_to_cogs_account_whole() -> bool:
            nonlocal new_sales_item, remaining_item_in_inventory

            leftover_sales_quantity = (
                new_sales_item.quantity - remaining_item_in_inventory.quantity
            )
            if leftover_sales_quantity <= 0:
                return False
            else:
                return True

        def _transfer_entire_batch_to_cogs_account():
            nonlocal cogs_list, inventory_list, new_sales_item

            cogs_list.append(copy.deepcopy(remaining_item_in_inventory))
            inventory_list.remove(remaining_item_in_inventory)
            new_sales_item.quantity -= remaining_item_in_inventory.quantity

        def _transfer_partial_batch_to_cogs_account_while_some_remains():
            nonlocal new_sales_item, remaining_item_in_inventory, remaining_item_in_inventory, cogs_list

            leftover_sales_quantity = (
                new_sales_item.quantity - remaining_item_in_inventory.quantity
            )

            sales_clone = copy.deepcopy(remaining_item_in_inventory)
            sales_clone.quantity += leftover_sales_quantity
            remaining_item_in_inventory.quantity -= sales_clone.quantity
            new_sales_item.quantity -= sales_clone.quantity
            cogs_list.append(sales_clone)

        def _has_already_transferred_all_new_sales() -> bool:
            nonlocal new_sales_item
            if new_sales_item.quantity == 0:
                return True
            else:
                return False

        def _is_selling_more_than_what_you_have() -> bool:
            nonlocal new_sales_item, inventory_list

            total_inventory_left = sum([y.quantity for y in inventory_list])

            if new_sales_item.quantity > total_inventory_left:
                return True
            else:
                return False

        for transaction_item in sorted_jobs_list.copy():
            if transaction_item.classification not in ("purchases", "sales"):
                continue
            if (transaction_item.classification == "purchases") and (
                transaction_item.classification != "sales"
            ):
                inventory_list.append(transaction_item)
                continue

            new_sales_item = transaction_item
            if _is_selling_more_than_what_you_have():
                raise SalesMoreThanInventoryError

            for remaining_item_in_inventory in inventory_list.copy():
                if _has_already_transferred_all_new_sales():
                    continue

                if _inventory_is_able_to_be_transfered_to_cogs_account_whole():
                    _transfer_entire_batch_to_cogs_account()
                else:
                    _transfer_partial_batch_to_cogs_account_while_some_remains()

        for i in inventory_list:
            if i.quantity == 0:
                inventory_list.remove(i)
        return cogs_list, inventory_list

    def cogs(self) -> float:
        """Calculates the cost of goods sold calculation from cogs_inventory method.

        Returns
        -------
        float
                        uses the result of the cogs_inventory method.
        """
        cost_of_goods_list, _ = self.cogs_inventory()
        cost_of_goods = [v.total_value for v in cost_of_goods_list]
        return sum(cost_of_goods)

    def leftover_inventory(self) -> list[Purchases]:
        """
        Outputs the leftover inventory after all transfers at the end of the month

        Returns
        -------
        list[Purchases]
            uses the result of the cogs_inventory method.
        """
        return self.cogs_inventory()[1]




def main():
    # a simple example to demonstrate the fifo inventory accounting method.
    p0 = Purchases("2024-05-01", 20, 3)
    # p0 is actually the beginning inventory at the beginning of the month.
    p1 = Purchases("2024-05-05", 5, 3.25)
    p2 = Purchases("2024-05-20", 7, 3.55)
    p3 = Purchases("2024-05-24", 5, 3.70)
    s1 = Sales("2024-05-13", 22, 10.00)
    s2 = Sales("2024-05-31", 13, 10.00)
    # s3 = Sales("2024-05-31", 2, 10.00)
    # s3 is used to demonstrate how we can get a consistent result even if we use the same date. This is the importance of the index attribute.
    i1 = Inventory([p0, p1, p2, p3], [s1, s2])
    print(i1.sorted_jobs_list)
    print(f"{i1.cogs()=:.2f}")
    print(f"{i1.leftover_inventory()=}")


if __name__ == "__main__":
    main()
