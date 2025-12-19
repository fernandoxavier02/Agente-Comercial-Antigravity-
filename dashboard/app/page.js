'use client';

import { useState, useEffect } from "react";
import { Gem, Plane, MapPin, BadgeDollarSign, ChevronRight, Activity, Star } from "lucide-react";

export default function LuxuryDashboard() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch leads from REAL database endpoint /leads
    const fetchLeads = async () => {
      try {
        setLoading(true);
        // Using the standard /leads endpoint which fetches from Database
        const response = await fetch('http://localhost:8000/leads');

        if (!response.ok) {
          throw new Error('Falha ao carregar leads do banco de dados');
        }

        const data = await response.json();

        // Transform database entities to dashboard format
        const transformedLeads = data.map(lead => ({
          id: lead.lead_id,
          name: lead.author_handle,
          wealth_score: lead.visual_analysis?.wealth_score || 0,
          visual_fit: lead.visual_analysis?.visual_fit_score || 0,
          location: extractLocation(lead.visual_analysis?.tags || []),
          assets: extractAssets(lead.visual_analysis?.tags || []),
          environment: extractEnvironment(lead.text_excerpt, lead.visual_analysis?.tags || []),
          // Use real photo from DB or fallback
          img: lead.profile_image_url || getPlaceholderImage(lead.visual_analysis?.wealth_score || 0),
          status: getStatus(lead.scores.lead_score),
          intent_layer: lead.intent_stage?.label || "discovery",
          source: lead.source
        }));

        // Sort by wealth_score descending
        transformedLeads.sort((a, b) => b.wealth_score - a.wealth_score);

        setLeads(transformedLeads);
        setError(null);
      } catch (err) {
        console.error('Erro ao buscar leads:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLeads();
  }, []);

  // Helper functions
  const extractLocation = (tags) => {
    if (!tags) return "São Paulo";
    const locationTag = tags.find(tag => tag.includes('_sp'));
    if (locationTag) {
      return locationTag.replace('_sp', '').replace('_', ' ').toUpperCase();
    }
    return "São Paulo";
  };

  const extractAssets = (tags) => {
    if (!tags) return [];
    return tags
      .filter(tag => tag.startsWith('dog_whistle:'))
      .map(tag => tag.replace('dog_whistle:', '').replace('_', ' '))
      .slice(0, 3);
  };

  const extractEnvironment = (text, tags) => {
    if (tags && tags.includes('dog_whistle:st_tropez')) return 'St. Tropez';
    if (text.toLowerCase().includes('st. tropez')) return 'St. Tropez';
    if (text.toLowerCase().includes('fasano')) return 'Hotel Fasano';
    if (text.toLowerCase().includes('jardins')) return 'Jardins, SP';
    if (text.toLowerCase().includes('itaim')) return 'Itaim Bibi, SP';
    return 'São Paulo';
  };

  const getPlaceholderImage = (wealthScore) => {
    if (wealthScore >= 90) {
      return "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=688&auto=format&fit=crop";
    } else if (wealthScore >= 70) {
      return "https://images.unsplash.com/photo-1616091216791-a5360b5fc78a?q=80&w=687&auto=format&fit=crop";
    } else {
      return "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=687&auto=format&fit=crop";
    }
  };

  const getStatus = (leadScore) => {
    if (leadScore >= 85) return "NEW";
    if (leadScore >= 70) return "CONTACTED";
    return "DISQUALIFIED";
  };

  return (
    <div className="min-h-screen bg-obsidian-900 text-platinum-100 font-sans selection:bg-gold-500 selection:text-white pb-20">
      <header className="fixed top-0 w-full z-50 bg-obsidian-900/80 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-gold-400 to-gold-200 flex items-center justify-center shadow-[0_0_15px_rgba(212,175,55,0.3)]">
              <span className="font-serif font-bold text-obsidian-900 text-lg">M</span>
            </div>
            <span className="font-serif text-2xl tracking-wide text-platinum-50">CLÍNICA <span className="text-gold-400">MAIS</span></span>
          </div>

          <nav className="hidden md:flex gap-8 text-sm font-medium text-platinum-400">
            <a href="#" className="text-gold-300 transition-colors">Wealth Radar</a>
            <a href="#" className="hover:text-white transition-colors">Concierge</a>
            <a href="#" className="hover:text-white transition-colors">Analytics</a>
          </nav>

          <div className="flex items-center gap-4">
            <div className="bg-obsidian-800 px-4 py-1.5 rounded-full border border-white/10 text-xs text-platinum-400 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              System Online
            </div>
          </div>
        </div>
      </header>

      <main className="pt-32 max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h1 className="font-serif text-5xl text-white mb-2 tracking-tight">Obsidian Radar<span className="text-gold-500">.</span></h1>
            <p className="text-platinum-400 font-light text-lg">
              Monitoramento de leads de <span className="text-gold-300">Ultra High Net Worth</span> em tempo real.
            </p>
          </div>
          <div className="flex gap-3">
            <button className="px-6 py-3 bg-obsidian-800 hover:bg-obsidian-700 border border-white/10 rounded-lg text-sm transition-all flex items-center gap-2">
              <Activity className="w-4 h-4 text-gold-400" />
              Live Feed
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-6 py-4 rounded-lg mb-8">
            ⚠️ Erro ao carregar leads: {error}. Verifique se o backend está rodando e conectado ao banco.
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center h-64 gap-4 animate-pulse">
            <div className="w-12 h-12 border-2 border-gold-500/30 border-t-gold-500 rounded-full animate-spin"></div>
            <span className="text-platinum-500 text-sm tracking-widest uppercase">Acessando Database Seguro...</span>
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {leads.map((lead) => (
              <div key={lead.id} className="group relative bg-obsidian-800 border border-white/5 rounded-2xl overflow-hidden hover:border-gold-500/30 transition-all duration-500 hover:shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                <div className="h-80 relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-t from-obsidian-900 via-transparent to-transparent z-10 opacity-90" />
                  <img src={lead.img} alt={lead.name} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                  <div className="absolute top-4 right-4 z-20">
                    {lead.wealth_score > 90 ? (
                      <span className="bg-gold-500/20 backdrop-blur-md border border-gold-500/50 text-gold-300 px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase flex items-center gap-1.5">
                        <Star className="w-3 h-3 fill-gold-500 text-gold-500" />
                        Ultra Luxury
                      </span>
                    ) : (
                      <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase backdrop-blur-md border ${lead.wealth_score < 50 ? 'bg-red-500/10 border-red-500/30 text-red-400' : 'bg-white/10 border-white/20 text-white'}`}>
                        {lead.wealth_score < 50 ? 'Disqualified' : 'Premium'}
                      </span>
                    )}
                  </div>
                  <div className="absolute top-4 left-4 z-20 flex items-center gap-1 text-xs font-medium text-white/80 bg-black/40 px-2 py-1 rounded backdrop-blur">
                    <MapPin className="w-3 h-3" /> {lead.location}
                  </div>
                </div>
                <div className="p-6 relative z-20 -mt-20">
                  <div className="flex justify-between items-end mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-white group-hover:text-gold-200 transition-colors">{lead.name}</h3>
                      <div className="text-xs text-platinum-400 uppercase tracking-wider mt-1 flex items-center gap-2">
                        {lead.environment}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-serif text-gold-400 font-bold">{lead.wealth_score}</div>
                      <div className="text-[10px] text-platinum-500 uppercase tracking-widest">Wealth Score</div>
                    </div>
                  </div>
                  {lead.assets.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-6">
                      {lead.assets.map(asset => (
                        <span key={asset} className="px-2 py-1 bg-white/5 border border-white/10 rounded text-[10px] text-platinum-300 uppercase tracking-wide">
                          {asset}
                        </span>
                      ))}
                    </div>
                  )}
                  <div className="pt-4 border-t border-white/5 flex items-center justify-between opacity-60 group-hover:opacity-100 transition-opacity">
                    <div className="flex gap-3">
                      <button className="p-2 hover:bg-white/10 rounded-full transition-colors text-platinum-400 hover:text-white" title="Mensagem">
                        <Gem className="w-4 h-4" />
                      </button>
                      <button className="p-2 hover:bg-white/10 rounded-full transition-colors text-platinum-400 hover:text-white" title="Ver Detalhes">
                        <Activity className="w-4 h-4" />
                      </button>
                    </div>
                    <button className="text-xs font-bold text-gold-400 flex items-center gap-1 hover:gap-2 transition-all">
                      INICIAR CONCIERGE <ChevronRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
