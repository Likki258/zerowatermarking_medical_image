import React, { useState } from 'react';
import { Search, Loader2, ShieldCheck, AlertTriangle, FileText, Download, QrCode } from 'lucide-react';

const Verify = () => {
  const [isVerifying, setIsVerifying] = useState(false);
  const [result, setResult] = useState<null | 'success' | 'failure'>(null);

  const startVerification = () => {
    setIsVerifying(true);
    setResult(null);
    setTimeout(() => {
      setIsVerifying(false);
      setResult('success'); // Simulation
    }, 2000);
  };

  return (
    <div className="max-w-5xl mx-auto py-10">
      <div className="mb-12">
        <h1 className="text-4xl font-extrabold mb-3 text-white">Verification <span className="text-[#4A90E2]">Portal</span></h1>
        <p className="text-gray-400">Validate medical image authenticity against the blockchain-anchored zero-watermark.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Verification Form */}
        <div className="glass-card p-10 space-y-8">
          <div>
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500 text-sm">01</span>
              Input Image for Analysis
            </h3>
            <div className="border-2 border-dashed border-white/10 rounded-2xl p-8 text-center hover:border-blue-500/50 cursor-pointer transition-colors">
              <QrCode className="w-12 h-12 text-blue-500/50 mx-auto mb-4" />
              <p className="text-sm font-bold opacity-80">Upload Patient Image or QR Token</p>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-500 text-sm">02</span>
              Identity Reference
            </h3>
            <div className="space-y-4">
              <input 
                type="text" 
                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 focus:border-blue-500 outline-none" 
                placeholder="Enter Transaction Hash or Image ID..." 
              />
              <button 
                onClick={startVerification}
                disabled={isVerifying}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 py-4 rounded-xl font-black text-lg flex items-center justify-center gap-3 transition-all"
              >
                {isVerifying ? (
                  <><Loader2 className="w-6 h-6 animate-spin" /> Analyzing Deep Features...</>
                ) : (
                  <><Search className="w-6 h-6" /> Initialize Verification</>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="glass-card p-10 flex items-center justify-center min-h-[400px]">
          {!result && !isVerifying && (
            <div className="text-center">
              <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6">
                <ShieldCheck className="w-12 h-12 text-gray-700" />
              </div>
              <h4 className="text-xl font-bold text-gray-500">Ready for Analysis</h4>
              <p className="text-sm text-gray-600 mt-2">Upload clinical data to begin.</p>
            </div>
          )}

          {isVerifying && (
            <div className="text-center animate-pulse">
              <div className="w-24 h-24 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <ShieldCheck className="w-12 h-12 text-blue-500" />
              </div>
              <h4 className="text-xl font-bold text-blue-500">Cross-Referencing Ledger</h4>
              <p className="text-sm text-gray-500 mt-2">Checking SHA-256 integrity...</p>
            </div>
          )}

          {result === 'success' && (
            <div className="w-full animate-in zoom-in-95 duration-500">
              <div className="text-center mb-10">
                <div className="w-28 h-28 bg-green-500/10 border-4 border-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                  <ShieldCheck className="w-16 h-16 text-green-500" />
                </div>
                <h4 className="text-3xl font-black text-green-500 tracking-tight">AUTHENTIC</h4>
                <p className="text-gray-400 mt-2 uppercase text-xs font-black tracking-widest leading-relaxed">Identity Verified on Blockchain</p>
              </div>

              <div className="bg-black/40 rounded-2xl p-6 border border-white/5 space-y-4">
                <ResultRow label="Image Reference" value="TX-9921-XRAY" />
                <ResultRow label="Similarity Score" value="99.98%" color="text-green-500" />
                <ResultRow label="Institutional Owner" value="City General Cardiology" />
                <ResultRow label="Anchor Block" value="#1,247,892" />
              </div>

              <div className="grid grid-cols-2 gap-4 mt-8">
                <button className="flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 py-3 rounded-xl text-sm font-bold">
                  <FileText className="w-4 h-4" /> Full Report
                </button>
                <button className="flex items-center justify-center gap-2 bg-green-600 hover:bg-green-500 py-3 rounded-xl text-sm font-bold">
                  <Download className="w-4 h-4" /> PDF Certificate
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const ResultRow = ({ label, value, color = "text-white" }) => (
  <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2 last:border-0 last:pb-0">
    <span className="text-gray-500 font-bold uppercase text-[10px] tracking-widest">{label}</span>
    <span className={`font-bold ${color}`}>{value}</span>
  </div>
);

export default Verify;
