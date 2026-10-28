export type User = {
  id: number;
  name: string;
  email: string;
  role: string;
};

export type Category = {
  id: number;
  name: string;
};

export type Product = {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category_id: number;
  category_name: string;
};

export type Transaction = {
  id: number;
  title: string;
  amount: number;
  total_amount: number;
  type: "income" | "expense";
  notes: string;
  transaction_date: string;
  product_id?: number | null;
};

export type Summary = {
  income: number;
  expense: number;
  balance: number;
  transaction_count: number;
  product_count: number;
};
