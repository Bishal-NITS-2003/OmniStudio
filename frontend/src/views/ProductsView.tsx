import React, { useState } from 'react';
import {
  Plus,
  Link2,
  Trash2,
  Search,
  ExternalLink,
  Upload,
  CheckCircle,
  ShoppingBag
} from 'lucide-react';
import type { Product, ProductImportResponse } from '../types';
import { Modal } from '../components/Modal';
import { api } from '../api/client';

interface ProductsViewProps {
  products: Product[];
  onRefresh: () => void;
  onToast: (type: 'success' | 'error' | 'warning' | 'info', msg: string) => void;
}

export const ProductsView: React.FC<ProductsViewProps> = ({
  products,
  onRefresh,
  onToast
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  // Manual Add Modal
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [newProduct, setNewProduct] = useState({
    name: '',
    tagline: '',
    description: '',
    category: 'Electronics',
    price: 4999.00,
    currency: 'Rs.',
    brand_name: 'OmniBrand',
    featuresText: 'High performance\nPremium build\nFast charging',
    image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'
  });

  // Import URL Modal
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [importUrl, setImportUrl] = useState('');
  const [isImporting, setIsImporting] = useState(false);
  const [importedPreview, setImportedPreview] = useState<ProductImportResponse | null>(null);

  // Filter products
  const filteredProducts = products.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'ALL' || p.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = ['ALL', ...Array.from(new Set(products.map((p) => p.category)))];

  // Handle Manual Product Creation
  const handleCreateProduct = async () => {
    if (!newProduct.name || !newProduct.description) {
      onToast('error', 'Product name and description are required');
      return;
    }

    try {
      const features = newProduct.featuresText
        .split('\n')
        .map((f) => f.trim())
        .filter(Boolean);

      await api.createProduct({
        name: newProduct.name,
        tagline: newProduct.tagline,
        description: newProduct.description,
        category: newProduct.category,
        price: Number(newProduct.price),
        currency: newProduct.currency,
        brand_name: newProduct.brand_name,
        features,
        image_urls: [newProduct.image_url]
      });

      onToast('success', `Product "${newProduct.name}" added to inventory`);
      setIsAddOpen(false);
      onRefresh();
    } catch (err: any) {
      onToast('error', err.message || 'Failed to create product');
    }
  };

  // Handle URL Scrape / Extraction
  const handleExtractUrl = async () => {
    if (!importUrl) {
      onToast('error', 'Please enter an Amazon, Flipkart, or e-commerce URL');
      return;
    }

    setIsImporting(true);
    try {
      const preview = await api.importProductUrl(importUrl);
      setImportedPreview(preview);
      onToast('info', `Extracted product specs from ${preview.extracted_source}. Please verify.`);
    } catch (err: any) {
      onToast('error', err.message || 'Failed to extract URL');
    } finally {
      setIsImporting(false);
    }
  };

  // Confirm Import
  const handleSaveImportedProduct = async () => {
    if (!importedPreview) return;
    try {
      await api.createProduct({
        name: importedPreview.name,
        tagline: importedPreview.tagline,
        description: importedPreview.description,
        category: importedPreview.category,
        price: importedPreview.price,
        currency: importedPreview.currency,
        brand_name: importedPreview.brand_name,
        features: importedPreview.features,
        image_urls: importedPreview.image_urls,
        source_url: importedPreview.source_url
      });

      onToast('success', `Imported "${importedPreview.name}" successfully!`);
      setIsImportOpen(false);
      setImportedPreview(null);
      setImportUrl('');
      onRefresh();
    } catch (err: any) {
      onToast('error', err.message || 'Failed to save imported product');
    }
  };

  // Handle Image Upload
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const res = await api.uploadProductImage(file);
      setNewProduct({ ...newProduct, image_url: res.url });
      onToast('success', 'Product photo uploaded successfully');
    } catch (err: any) {
      onToast('error', 'Image upload failed');
    }
  };

  const handleDeleteProduct = async (id: number, name: string) => {
    if (!confirm(`Delete "${name}" from inventory?`)) return;
    try {
      await api.deleteProduct(id);
      onToast('success', `Deleted ${name}`);
      onRefresh();
    } catch (err: any) {
      onToast('error', 'Failed to delete product');
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Product Inventory</h1>
          <p className="page-subtitle">
            Manage catalog items or import from Amazon, Flipkart, and store URLs
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            id="import-url-btn"
            className="btn btn-secondary"
            onClick={() => setIsImportOpen(true)}
          >
            <Link2 size={16} /> Import from URL
          </button>
          <button
            id="add-product-btn"
            className="btn btn-primary"
            onClick={() => setIsAddOpen(true)}
          >
            <Plus size={16} /> Add Product
          </button>
        </div>
      </div>

      <div style={{
        display: 'flex',
        gap: '16px',
        alignItems: 'center',
        marginBottom: '28px',
        flexWrap: 'wrap'
      }}>
        <div style={{ position: 'relative', flex: 1, minWidth: '240px' }}>
          <Search size={16} style={{ position: 'absolute', left: '14px', top: '15px', color: '#94a3b8' }} />
          <input
            id="product-search-input"
            type="text"
            className="form-control"
            placeholder="Search products by title, feature, or keyword..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ paddingLeft: '40px' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto' }}>
          {categories.map((cat) => (
            <button
              key={cat}
              className={`btn btn-sm ${selectedCategory === cat ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {filteredProducts.length === 0 ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <ShoppingBag size={48} color="#6366f1" style={{ margin: '0 auto 16px' }} />
          <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '6px' }}>No Products Found</h3>
          <p style={{ color: '#94a3b8', fontSize: '14px', marginBottom: '20px' }}>
            Try adjusting your search filters or import products directly from Amazon or Flipkart.
          </p>
          <button className="btn btn-primary" onClick={() => setIsImportOpen(true)}>
            <Link2 size={16} /> Import from URL
          </button>
        </div>
      ) : (
        <div className="grid-3">
          {filteredProducts.map((p) => {
            const primaryImg = p.image_urls?.[0] || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80';
            return (
              <div key={p.id} className="product-card">
                <div className="product-thumb">
                  <img src={primaryImg} alt={p.name} />
                  <div className="product-price-pill">
                    Rs. {p.price.toLocaleString('en-IN')}
                  </div>
                </div>

                <div className="product-body">
                  <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#818cf8', fontWeight: 700, marginBottom: '4px' }}>
                    {p.brand_name} • {p.category}
                  </div>
                  <h3 className="product-name">{p.name}</h3>
                  <p className="product-desc">{p.description}</p>

                  <div className="product-features-tags">
                    {(p.features || []).slice(0, 3).map((feat, i) => (
                      <span key={i} className="feature-pill">✓ {feat}</span>
                    ))}
                  </div>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    borderTop: '1px solid var(--border-subtle)',
                    paddingTop: '14px',
                    marginTop: 'auto'
                  }}>
                    {p.source_url ? (
                      <a
                        href={p.source_url}
                        target="_blank"
                        rel="noreferrer"
                        style={{ fontSize: '12px', color: '#38bdf8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
                      >
                        <ExternalLink size={13} /> Source Link
                      </a>
                    ) : (
                      <span style={{ fontSize: '12px', color: '#64748b' }}>Custom SKU</span>
                    )}

                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDeleteProduct(p.id, p.name)}
                      title="Delete Product"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Manual Add Product Modal */}
      <Modal
        isOpen={isAddOpen}
        onClose={() => setIsAddOpen(false)}
        title="Add Product to Inventory"
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setIsAddOpen(false)}>Cancel</button>
            <button className="btn btn-primary" onClick={handleCreateProduct}>Save Product</button>
          </>
        }
      >
        <div className="form-group">
          <label className="form-label">Product Name *</label>
          <input
            className="form-control"
            placeholder="e.g. AeroPulse Wireless ANC Headphones"
            value={newProduct.name}
            onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Tagline</label>
          <input
            className="form-control"
            placeholder="e.g. Immersive Sound, 40-Hour Battery"
            value={newProduct.tagline}
            onChange={(e) => setNewProduct({ ...newProduct, tagline: e.target.value })}
          />
        </div>

        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Category</label>
            <input
              className="form-control"
              value={newProduct.category}
              onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Brand Name</label>
            <input
              className="form-control"
              value={newProduct.brand_name}
              onChange={(e) => setNewProduct({ ...newProduct, brand_name: e.target.value })}
            />
          </div>
        </div>

        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Price</label>
            <input
              type="number"
              className="form-control"
              value={newProduct.price}
              onChange={(e) => setNewProduct({ ...newProduct, price: parseFloat(e.target.value) || 0 })}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Currency</label>
            <input
              className="form-control"
              value={newProduct.currency}
              onChange={(e) => setNewProduct({ ...newProduct, currency: e.target.value })}
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Description *</label>
          <textarea
            className="form-control"
            rows={3}
            placeholder="Detailed description of specs, materials, and benefits..."
            value={newProduct.description}
            onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Key Features (one per line)</label>
          <textarea
            className="form-control"
            rows={3}
            value={newProduct.featuresText}
            onChange={(e) => setNewProduct({ ...newProduct, featuresText: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Product Image (URL or Upload)</label>
          <input
            className="form-control"
            placeholder="https://images.unsplash.com/..."
            value={newProduct.image_url}
            onChange={(e) => setNewProduct({ ...newProduct, image_url: e.target.value })}
            style={{ marginBottom: '8px' }}
          />
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <label className="btn btn-secondary btn-sm" style={{ cursor: 'pointer' }}>
              <Upload size={14} /> Upload Local Image
              <input type="file" accept="image/*" onChange={handleFileUpload} style={{ display: 'none' }} />
            </label>
            <span style={{ fontSize: '11px', color: '#94a3b8' }}>PNG, JPG or WebP</span>
          </div>
        </div>
      </Modal>

      {/* URL Importer & Verification Modal */}
      <Modal
        isOpen={isImportOpen}
        onClose={() => {
          setIsImportOpen(false);
          setImportedPreview(null);
        }}
        title="Import Product from E-Commerce URL"
        footer={
          importedPreview ? (
            <>
              <button className="btn btn-secondary" onClick={() => setImportedPreview(null)}>
                Back
              </button>
              <button className="btn btn-success" onClick={handleSaveImportedProduct}>
                <CheckCircle size={16} /> Confirm & Save to Inventory
              </button>
            </>
          ) : (
            <button className="btn btn-primary" onClick={handleExtractUrl} disabled={isImporting}>
              {isImporting ? 'Extracting Product...' : 'Extract Specifications'}
            </button>
          )
        }
      >
        {!importedPreview ? (
          <div>
            <p style={{ fontSize: '14px', color: '#cbd5e1', marginBottom: '16px' }}>
              Paste an Amazon, Flipkart, or e-commerce link. OmniPost extracts title, bullet points,
              pricing, and high-res imagery with a verification gate.
            </p>
            <div className="form-group">
              <label className="form-label">Product URL</label>
              <input
                id="url-import-input"
                className="form-control"
                placeholder="https://www.amazon.com/dp/... or https://www.flipkart.com/..."
                value={importUrl}
                onChange={(e) => setImportUrl(e.target.value)}
              />
            </div>

            <div style={{
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid rgba(99, 102, 241, 0.25)',
              borderRadius: '8px',
              padding: '12px 16px',
              fontSize: '12px',
              color: '#c7d2fe'
            }}>
              💡 <strong>Quick Test Presets:</strong> You can paste any live product link, or type <code>amazon.com/headphones</code> or <code>flipkart.com/watch</code> to demo instant extraction.
            </div>
          </div>
        ) : (
          <div>
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(16, 185, 129, 0.2)',
              color: '#34d399',
              padding: '4px 10px',
              borderRadius: 'var(--radius-full)',
              fontSize: '11px',
              fontWeight: 700,
              marginBottom: '14px'
            }}>
              <CheckCircle size={13} /> Extracted from {importedPreview.extracted_source} ({Math.round(importedPreview.confidence_score * 100)}% Confidence)
            </div>

            <div className="form-group">
              <label className="form-label">Verified Title</label>
              <input
                className="form-control"
                value={importedPreview.name}
                onChange={(e) => setImportedPreview({ ...importedPreview, name: e.target.value })}
              />
            </div>

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Brand</label>
                <input
                  className="form-control"
                  value={importedPreview.brand_name}
                  onChange={(e) => setImportedPreview({ ...importedPreview, brand_name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Price ({importedPreview.currency})</label>
                <input
                  type="number"
                  className="form-control"
                  value={importedPreview.price}
                  onChange={(e) => setImportedPreview({ ...importedPreview, price: parseFloat(e.target.value) || 0 })}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Extracted Description</label>
              <textarea
                className="form-control"
                rows={3}
                value={importedPreview.description}
                onChange={(e) => setImportedPreview({ ...importedPreview, description: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Extracted Features</label>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {importedPreview.features.map((feat, i) => (
                  <div key={i} style={{ fontSize: '12px', background: 'rgba(255, 255, 255, 0.04)', padding: '6px 10px', borderRadius: '6px', color: '#cbd5e1' }}>
                    • {feat}
                  </div>
                ))}
              </div>
            </div>

            {importedPreview.image_urls.length > 0 && (
              <div className="form-group">
                <label className="form-label">Product Image Preview</label>
                <img
                  src={importedPreview.image_urls[0]}
                  alt="Extracted preview"
                  style={{ width: '100px', height: '100px', objectFit: 'cover', borderRadius: '8px' }}
                />
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};
