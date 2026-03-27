import React, { useState } from 'react';
import { Upload, ChevronRight, CheckCircle2, ShieldCheck, Lock, Database } from 'lucide-react';

const Register = () => {
  const [step, setStep] = useState(1);

  return (
    <div className="max-w-4xl mx-auto py-10">
      <div className="flex items-center justify-between mb-12">
        <div>
          <h1 className="text-4xl font-extrabold mb-3">Register <span className="text-[#26C6DA]">Medical Image</span></h1>
          <p className="text-gray-400">Anchor your clinical data on the immutable blockchain ledger.</p>
        </div>
        <div className="flex items-center gap-2">
          {[1, 2, 3, 4].map(s => (
            <div key={s} className={`w-3 h-3 rounded-full transition-all duration-500 ${step >= s ? 'bg-[#26C6DA] w-10' : 'bg-white/10'}`}></div>
          ))}
        </div>
      </div>

      <div className="glass-card p-10">
        {step === 1 && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold mb-8 flex items-center gap-3">
              <span className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-[#26C6DA]">1</span>
              Upload Medical Image
            </h2>
            <div className="border-2 border-dashed border-white/10 rounded-3xl p-20 text-center hover:border-[#26C6DA]/50 transition-colors cursor-pointer group">
              <div className="w-20 h-20 bg-[#26C6DA]/10 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                <Upload className="text-[#26C6DA] w-10 h-10" />
              </div>
              <p className="text-xl font-bold mb-2">Drag & Drop DICOM or X-Ray</p>
              <p className="text-gray-500">Supported formats: JPEG, PNG, DICOM (Max 50MB)</p>
            </div>
            <div className="flex justify-end mt-10">
              <button 
                onClick={() => setStep(2)}
                className="bg-[#26C6DA] hover:bg-[#1fb8cc] px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-transform active:scale-95"
              >
                Continue <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold mb-8 flex items-center gap-3">
              <span className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-[#26C6DA]">2</span>
              Configure Security
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-2">
                <label className="text-xs font-black uppercase tracking-widest text-gray-500">Hospital Reference</label>
                <input type="text" className="w-full bg-white/5 border border-white/10 rounded-xl p-4 focus:border-[#26C6DA] outline-none" placeholder="HOSP-2024-001" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-black uppercase tracking-widest text-gray-500">Modality</label>
                <select className="w-full bg-white/5 border border-white/10 rounded-xl p-4 focus:border-[#26C6DA] outline-none appearance-none">
                  <option>Chest X-Ray</option>
                  <option>Brain MRI</option>
                  <option>Cardiac CT</option>
                </select>
              </div>
              <div className="md:col-span-2 p-6 bg-white/5 border border-white/10 rounded-2xl flex items-start gap-4">
                <ShieldCheck className="text-[#26C6DA] w-6 h-6 shrink-0 mt-1" />
                <div>
                  <p className="font-bold text-sm">Automated Zero-Watermarking</p>
                  <p className="text-xs text-gray-500 leading-relaxed mt-1">
                    The ResNet-50 engine will automatically extract 2048 deep features and encrypt them using a 15-digit Collatz chaotic seed. Original pixels will remain untouched.
                  </p>
                </div>
              </div>
            </div>
            <div className="flex justify-between mt-10">
              <button onClick={() => setStep(1)} className="text-gray-400 font-bold px-8">Back</button>
              <button onClick={() => setStep(3)} className="bg-[#26C6DA] hover:bg-[#1fb8cc] px-8 py-3 rounded-xl font-bold flex items-center gap-2">Final Review <ChevronRight className="w-5 h-5" /></button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold mb-8 text-center uppercase tracking-tight">Review & <span className="text-[#26C6DA]">Verify</span></h2>
            <div className="space-y-4 mb-10">
              <div className="flex justify-between p-6 bg-white/5 rounded-2xl border border-white/10">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center">
                    <Database className="text-[#26C6DA] w-6 h-6 " />
                  </div>
                  <div>
                    <p className="text-xs font-black text-gray-500 uppercase">Blockchain Network</p>
                    <p className="font-bold">MediShield Global Ledger</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs font-black text-gray-500 uppercase">Gas Fee</p>
                  <p className="font-bold text-[#4CAF50]">0.0023 ETH</p>
                </div>
              </div>

              <div className="p-6 bg-[#26C6DA]/5 border border-[#26C6DA]/20 rounded-2xl">
                <div className="flex items-center gap-2 text-[#26C6DA] mb-3">
                  <Lock className="w-4 h-4" />
                  <p className="text-xs font-black uppercase tracking-widest">Privacy Compliance</p>
                </div>
                <p className="text-sm text-gray-400 leading-relaxed italic">
                  "I certify that this image contains no PII and complies with institutional data sharing protocols."
                </p>
              </div>
            </div>
            <div className="flex justify-between">
              <button onClick={() => setStep(2)} className="text-gray-400 font-bold px-8">Back</button>
              <button className="bg-gradient-to-r from-[#26C6DA] to-[#7B68EE] px-10 py-4 rounded-2xl font-black text-lg shadow-xl shadow-blue-500/20 active:scale-95 transition-transform">
                AUTHORIZE REGISTRATION
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Register;
