import React, { useState, useEffect, useCallback, type ChangeEvent } from 'react';
import './RegisterLastTransaction.css';
import { useApiService } from '../../services/apiService';

const API_URL = import.meta.env.VITE_API_URL;

type Transaction = {
  asset?: string;
  fiat?: string;
  amount?: number;
  unitPrice?: number | string;
  orderCreatedAt?: number | string;
  createTime?: number | string;
};

type Category = {
  _id: string;
  name: string;
};

const RegisterLastTransaction: React.FC = () => {
  const { callApi } = useApiService();
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [categoryLoading, setCategoryLoading] = useState(false);
  const [categoryError, setCategoryError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);
  const fetchCategories = useCallback(async () => {
    setCategoryLoading(true);
    setCategoryError(null);
    try {
      const data = await callApi(`${API_URL}/category/all`, { method: 'GET' });
      setCategories(data);
    } catch (err: any) {
      setCategoryError('Failed to fetch categories');
    } finally {
      setCategoryLoading(false);
    }
  }, [callApi]);

  useEffect(() => {
    fetchCategories();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchLastTransaction = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await callApi(`${API_URL}/transaction/get_last_transaction`, { method: 'GET' });
      setTransaction(data);
    } catch (err: any) {
      setError('Failed to fetch transaction');
      setTransaction(null);
    } finally {
      setLoading(false);
    }
  };


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!transaction || !selectedCategory || !description.trim()) return;
    setSubmitLoading(true);
    setSubmitError(null);
    setSubmitSuccess(null);
    try {
      // Extract and convert fields from transaction
      const unitPrice = transaction.unitPrice ? parseFloat(transaction.unitPrice as any) : undefined;
      const orderCreatedAt = transaction.orderCreatedAt
        ? new Date(Number(transaction.orderCreatedAt)).toISOString()
        : new Date().toISOString();
      const createTime = transaction.createTime ? Number(transaction.createTime) : undefined;

      const payload: any = {
        amount: transaction.amount,
        unitPrice,
        fiat: transaction.fiat,
        description,
        orderCreatedAt,
        category_id: selectedCategory,
      };
      if (createTime) payload.createTime = createTime;

      await callApi(`${API_URL}/transaction/create`, {
        method: 'POST',
        data: payload,
      });
      setSubmitSuccess('Transaction registered successfully!');
      setDescription('');
      setSelectedCategory('');
    } catch (err: any) {
      setSubmitError('Failed to register transaction');
    } finally {
      setSubmitLoading(false);
    }
  };

  return (
    <div className="register-last-transaction">
      <h2>Register Last Transaction</h2>
      <div className="register-last-transaction__btn-wrapper">
        <button className="btn" onClick={fetchLastTransaction} disabled={loading}>
          {loading ? 'Loading...' : 'Get Last Transaction'}
        </button>
      </div>
      {error && <div className="register-last-transaction__error">{error}</div>}
      <table className="register-last-transaction__table">
        <thead>
          <tr>
            <th className="register-last-transaction__th">Asset</th>
            <th className="register-last-transaction__th">Fiat</th>
            <th className="register-last-transaction__th">Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="register-last-transaction__td">{transaction?.asset || ''}</td>
            <td className="register-last-transaction__td">{transaction?.fiat || ''}</td>
            <td className="register-last-transaction__td">{transaction?.amount ?? ''}</td>
          </tr>
        </tbody>
      </table>
      <form onSubmit={handleSubmit} className="register-last-transaction__form">
        <div className="register-last-transaction__form-group">
          <label htmlFor="category-select" className="register-last-transaction__label">Category:</label>
          <select
            id="category-select"
            value={selectedCategory}
            onChange={e => setSelectedCategory(e.target.value)}
            disabled={categoryLoading || submitLoading}
            className="register-last-transaction__select"
            required
          >
            <option value="">{categoryLoading ? 'Loading...' : '-- Select Category --'}</option>
            {categories.map(cat => (
              <option key={cat._id} value={cat._id}>{cat.name}</option>
            ))}
          </select>
          {categoryError && <span className="register-last-transaction__category-error">{categoryError}</span>}
        </div>
        <div className="register-last-transaction__form-group">
          <label htmlFor="description" className="register-last-transaction__label">Description:</label>
          <input
            id="description"
            type="text"
            value={description}
            onChange={e => setDescription(e.target.value)}
            className="register-last-transaction__input"
            placeholder="Enter description"
            required
          />
        </div>
        <div className="register-last-transaction__submit-btn-wrapper">
          <button
            className="btn"
            type="submit"
            disabled={
              submitLoading ||
              !transaction ||
              !selectedCategory ||
              !description.trim()
            }
          >
            {submitLoading ? 'Submitting...' : 'Submit'}
          </button>
        </div>
        {submitError && <div className="register-last-transaction__submit-error">{submitError}</div>}
        {submitSuccess && <div className="register-last-transaction__submit-success">{submitSuccess}</div>}
      </form>
    </div>
  );
};

export default RegisterLastTransaction;
