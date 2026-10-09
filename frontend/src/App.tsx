import { useState, useEffect } from 'react';
import type { Product, BrandKit, Campaign, AnalyticsOverview } from './types';
import { api } from './api/client';
import { Navbar } from './components/Navbar';
import { Toast, type ToastMessage } from './components/Toast';

import { DashboardView } from './views/DashboardView';
import { ProductsView } from './views/ProductsView';
import { CampaignBuilderView } from './views/CampaignBuilderView';
import { CampaignDetailView } from './views/CampaignDetailView';
import { BrandKitView } from './views/BrandKitView';
import { PublishingView } from './views/PublishingView';

export function App() {
  const [currentView, setCurrentView] = useState<string>('dashboard');
  const [selectedCampaignId, setSelectedCampaignId] = useState<number | null>(null);

  const [products, setProducts] = useState<Product[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [brandKit, setBrandKit] = useState<BrandKit | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null);

  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (type: 'success' | 'warning' | 'error' | 'info', message: string) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      dismissToast(id);
    }, 4500);
  };

  const dismissToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const loadData = async () => {
    try {
      const [prods, camps, bk, an] = await Promise.all([
        api.getProducts().catch(() => []),
        api.getCampaigns().catch(() => []),
        api.getBrandKit().catch(() => null),
        api.getAnalytics().catch(() => null)
      ]);
      setProducts(prods);
      setCampaigns(camps);
      setBrandKit(bk);
      setAnalytics(an);
    } catch (err: any) {
      console.error('Initialization error:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectCampaign = (id: number) => {
    setSelectedCampaignId(id);
    setCurrentView('campaign-detail');
  };

  const handleCampaignCreated = (id: number) => {
    loadData();
    setSelectedCampaignId(id);
    setCurrentView('campaign-detail');
  };

  return (
    <div className="app-container">
      {/* Sidebar Navbar */}
      <Navbar
        currentView={currentView}
        onNavigate={(view) => {
          setCurrentView(view);
          if (view !== 'campaign-detail') {
            setSelectedCampaignId(null);
          }
        }}
        campaignsCount={campaigns.length}
      />

      {/* Main Content Area */}
      <main className="main-content">
        {currentView === 'dashboard' && (
          <DashboardView
            analytics={analytics}
            campaigns={campaigns}
            onSelectCampaign={handleSelectCampaign}
            onNavigate={(view) => setCurrentView(view)}
          />
        )}

        {currentView === 'products' && (
          <ProductsView
            products={products}
            onRefresh={loadData}
            onToast={addToast}
          />
        )}

        {currentView === 'builder' && (
          <CampaignBuilderView
            products={products}
            brandKit={brandKit}
            onCampaignCreated={handleCampaignCreated}
            onToast={addToast}
          />
        )}

        {currentView === 'campaign-detail' && selectedCampaignId && (
          <CampaignDetailView
            campaignId={selectedCampaignId}
            onBack={() => {
              setCurrentView('dashboard');
              loadData();
            }}
            onToast={addToast}
          />
        )}

        {currentView === 'brandkit' && (
          <BrandKitView
            brandKit={brandKit}
            onRefresh={loadData}
            onToast={addToast}
          />
        )}

        {currentView === 'publishing' && (
          <PublishingView
            campaigns={campaigns}
            onToast={addToast}
          />
        )}
      </main>

      {/* Global Notifications */}
      <Toast toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}

export default App;
