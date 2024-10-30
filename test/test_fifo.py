import unittest
import os
import sys
# include parent directory as well
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fifo import Sales, Purchases, Inventory, SalesMoreThanInventoryError
import datetime as dt

class TestPurchases(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.p0 = Purchases("2023-03-07", 10, 3.00)
		self.p1 = Purchases("2023-04-09", 11, 4.00)
		self.p2 = Purchases("2023-03-07", 17, 2.50)
		self.p3 = Purchases(dt.date(2024, 5, 4), 29, 10.00)

	def tearDown(self) -> None:
		super().tearDown()
		Purchases._reset_index()

	def test_date_returns(self):
		self.assertGreater(self.p1.date_iso, self.p0.date_iso)
		self.assertEqual(self.p0.date_iso, self.p2.date_iso)
		self.assertLess(self.p2.date_iso, self.p1.date_iso)
		self.assertIsInstance(self.p0.date_iso, dt.date)
		self.assertIsInstance(self.p3.date_iso, dt.date)

		with self.assertRaises(ValueError):
			Purchases("2023-02-29", 14, 2.00)

		with self.assertRaises(ValueError):
			Purchases("2024-04-31", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("2100-02-29", 30, 15.00)

		with self.assertRaises(ValueError):
			Purchases("2015-31-05", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("31-05-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Purchases("2019-3-01", 10, 3.00)

	def test_index(self):
		self.assertEqual(self.p0.index, 0)
		self.assertEqual(self.p1.index, 1)

	def test_slots(self):
		with self.assertRaises(AttributeError):
			self.p0.hello = "hello"

	def test_postive(self):
		Purchases("2024-07-23", 0, 10.00)
		Purchases("2024-07-23", 10, 0.00)
		Purchases("2024-07-23", 10, 0)
		Purchases("2024-07-23", 0, 0)
		with self.assertRaises(ValueError):
			Purchases("2019-03-01", -10, 3.00)
		with self.assertRaises(ValueError):
			Purchases("2019-03-01", 10, -3.00)
		with self.assertRaises(ValueError):
			Purchases("2019-03-01", -10, -3.00)\
			
	def test_frozen(self):
		with self.assertRaises(AttributeError):
			self.p0.unit_price = 10.30
		with self.assertRaises(AttributeError):
			self.p1.date_iso = '2023-04-07'
		with self.assertRaises(AttributeError):
			self.p2.classification = 'Hello'
		with self.assertRaises(AttributeError):
			self.p3.index_global = "Hello"
		


class TestSales(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.s0 = Sales("2023-03-07", 10, 3.00)
		self.s1 = Sales("2023-04-09", 11, 4.00)
		self.s2 = Sales("2023-03-07", 17, 2.50)
		self.s3 = Sales(dt.date(2024, 5, 4), 29, 10.00)

	def tearDown(self) -> None:
		super().tearDown()
		Sales._reset_index()

	def test_date_returns(self):
		self.assertGreater(self.s1.date_iso, self.s0.date_iso)
		self.assertEqual(self.s0.date_iso, self.s2.date_iso)
		self.assertLess(self.s2.date_iso, self.s1.date_iso)
		self.assertIsInstance(self.s0.date_iso, dt.date)
		self.assertIsInstance(self.s3.date_iso, dt.date)

		with self.assertRaises(ValueError):
			Sales("2023-02-29", 14, 2.00)

		with self.assertRaises(ValueError):
			Sales("2024-04-31", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("2100-02-29", 30, 15.00)

		with self.assertRaises(ValueError):
			Sales("2015-31-05", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("31-05-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("05-20-2024", 10, 3.00)

		with self.assertRaises(ValueError):
			Sales("2019-3-01", 10, 3.00)

	def test_index(self):
		self.assertEqual(self.s0.index, 0)
		self.assertEqual(self.s1.index, 1)

	def test_slots(self):
		with self.assertRaises(AttributeError):
			self.s0.hello = "hello"
	
	def test_postive(self):
		Sales("2024-07-23", 0, 10.00)
		Sales("2024-07-23", 10, 0.00)
		Sales("2024-07-23", 10, 0)
		Sales("2024-07-23", 0, 0)
		with self.assertRaises(ValueError):
			Sales("2019-03-01", -10, 3.00)
		with self.assertRaises(ValueError):
			Sales("2019-03-01", 10, -3.00)
		with self.assertRaises(ValueError):
			Sales("2019-03-01", -10, -3.00)

	def test_frozen(self):
		with self.assertRaises(AttributeError):
			self.s0.unit_price = 10.30
		with self.assertRaises(AttributeError):
			self.s1.date_iso = '2023-04-07'
		with self.assertRaises(AttributeError):
			self.s2.classification = 'Hello'
		with self.assertRaises(AttributeError):
			self.s3.index_global = "Hello"


class TestInventory(unittest.TestCase):
	def setUp(self) -> None:
		super().setUp()
		self.p0 = Purchases("2024-05-01", 20, 3)
		self.p1 = Purchases("2024-05-05", 5, 3.25)
		self.p2 = Purchases("2024-05-20", 7, 3.55)
		self.p3 = Purchases("2024-05-24", 5, 3.70)
		self.p4 = Purchases("2024-05-24", 10, 3.60)
		self.p5 = Purchases("2024-05-31", 13, 2.50)
		self.s1 = Sales("2024-05-13", 22, 10.00)
		self.s2 = Sales("2024-05-13", 7, 11.00)
		self.s3 = Sales("2024-05-31", 13, 10.00)
		self.s4 = Sales("2024-05-31", 4, 11.00)
		self.i1 = Inventory([self.p0, self.p1, self.p2, self.p3], [self.s1, self.s3])
		self.i2 = Inventory([self.p0, self.p1, self.p2, self.p3, self.p4], [self.s1, self.s2, self.s3, self.s4])
	def tearDown(self) -> None:
		return super().tearDown()

	def test_date_index_order(self):
		self.sorted_inventory_list = [self.p0, self.p1, self.s1, self.s2, self.p2, self.p3, self.p4, self.s3, self.s4]
		self.assertEqual(self.sorted_inventory_list, self.i2.sorted_jobs_list)
		self.shuffled_inventory = Inventory([self.p0, self.p1, self.p2, self.p3, self.p4], [self.s3, self.s4, self.s2, self.s1])
		self.assertEqual(self.i2.purchase_list_sorted, self.shuffled_inventory.purchase_list_sorted)
		self.assertEqual(self.i2.sales_list_sorted, self.shuffled_inventory.sales_list_sorted)
	
	def test_cogs(self):
		self.assertEqual(self.i1.cogs(), 112.20)

	def test_oversold(self):
		with self.assertRaises(SalesMoreThanInventoryError):
			Inventory([self.p1], [self.s1]).cogs()
	
	def test_sales_revenue(self):
		self.assertEqual(self.i1.sales_revenue(), 350.00)

if __name__ == "__main__":
	unittest.main()
