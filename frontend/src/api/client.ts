import type {
  Product,
  ProductImportResponse,
  BrandKit,
  Campaign,
  PublishingAccount,
  PublishingLog,
  AnalyticsOverview
} from '../types';

const BASE_URL = '/api';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {})
    }
  });

  if (!res.ok) {
    let errorMsg = `HTTP Error ${res.status}`;
    try {
      const err = await res.json();
      if (err.detail) errorMsg = err.detail;
    } catch {}
    throw new Error(errorMsg);
  }

  return res.json();
}

export const api = {
  // Products
  getProducts: () => fetchJson<Product[]>('/products'),
  getProduct: (id: number) => fetchJson<Product>(`/products/${id}`),
  createProduct: (data: Partial<Product>) => fetchJson<Product>('/products', { method: 'POST', body: JSON.stringify(data) }),
  updateProduct: (id: number, data: Partial<Product>) => fetchJson<Product>(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteProduct: (id: number) => fetchJson<{ message: string }>(`/products/${id}`, { method: 'DELETE' }),
  importProductUrl: (url: string) => fetchJson<ProductImportResponse>('/products/import-url', { method: 'POST', body: JSON.stringify({ url }) }),
  uploadProductImage: async (file: File): Promise<{ filename: string; url: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${BASE_URL}/products/upload-image`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Image upload failed');
    return res.json();
  },

  // Brand Kit
  getBrandKit: () => fetchJson<BrandKit>('/brand-kit'),
  updateBrandKit: (data: Partial<BrandKit>) => fetchJson<BrandKit>('/brand-kit', { method: 'PUT', body: JSON.stringify(data) }),

  // Campaigns & LangGraph
  getCampaigns: () => fetchJson<Campaign[]>('/campaigns'),
  getCampaign: (id: number) => fetchJson<Campaign>(`/campaigns/${id}`),
  createCampaign: (data: any) => fetchJson<Campaign>('/campaigns', { method: 'POST', body: JSON.stringify(data) }),
  triggerGenerate: (id: number) => fetchJson<Campaign>(`/campaigns/${id}/generate`, { method: 'POST' }),
  approveCampaign: (id: number, approved: boolean, feedback?: string) =>
    fetchJson<Campaign>(`/campaigns/${id}/approve`, { method: 'POST', body: JSON.stringify({ approved, feedback }) }),
  publishCampaign: (id: number, platforms?: string[]) =>
    fetchJson<Campaign>(`/campaigns/${id}/publish`, { method: 'POST', body: JSON.stringify({ platforms }) }),
  deleteCampaign: (id: number) => fetchJson<{ message: string }>(`/campaigns/${id}`, { method: 'DELETE' }),

  // Publishing
  getPublishingAccounts: () => fetchJson<PublishingAccount[]>('/publishing/accounts'),
  connectAccount: (data: any) => fetchJson<PublishingAccount>('/publishing/accounts/connect', { method: 'POST', body: JSON.stringify(data) }),
  getPublishingLogs: () => fetchJson<PublishingLog[]>('/publishing/logs'),
  getDownloadUrl: (campaignId: number) => `${BASE_URL}/publishing/download/${campaignId}`,

  // Analytics
  getAnalytics: () => fetchJson<AnalyticsOverview>('/analytics/overview')
};
