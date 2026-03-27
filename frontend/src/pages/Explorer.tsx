import React from 'react';
import { Box, Hash, Clock, Cpu, Search, ArrowUpRight } from 'lucide-react';

const Explorer = () => {
  return (
    <div className="space-y-10 py-10">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-extrabold mb-3">Blockchain <span className="text-[#7B68EE]">Explorer</span></h1>
          <p className="text-gray-400">Deep search of the immutable medical provenance ledger.</p>
        </div>
        <div className="flex gap-4">
          <div className="glass-card px-6 py-3 flex items-center gap-3">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-black tracking-widest text-[#7B68EE]">LIVE STATUS</span>
          </div>
        </div>
      </header>

      {/* Network Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ExplorerStat label="Chain Height" value="1,247,892" icon={Box} />
        <ExplorerStat label="Avg. TPS" value="12.4" icon={Cpu} />
        <ExplorerStat label="Total Volume" value="4.8M TX" icon={Hash} />
        <ExplorerStat label="Latency" value="12ms" icon={Clock} />
      </div>

      {/* Search Bar */}
      <div className="glass-card p-4 flex items-center gap-4 border-2 border-[#7B68EE]/20">
        <Search className="text-gray-500 w-6 h-6 ml-4" />
        <input 
          type="text" 
          placeholder="Search by Transaction Hash, Block, or Image ID..." 
          className="flex-1 bg-transparent border-none outline-none text-xl placeholder:text-gray-700" 
        />
        <button className="bg-[#7B68EE] hover:bg-[#6a56e0] px-8 py-3 rounded-xl font-bold transition-all">
          Locate Block
        </button>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-10">
        {/* Latest Blocks */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-3">
            <Box className="w-6 h-6 text-[#7B68EE]" /> Latest Validated Blocks
          </h3>
          <div className="space-y-4">
            <BlockCard index="1,247,892" txs="12" size="4.2MB" validator="Hosp_01" time="32s ago" />
            <BlockCard index="1,247,891" txs="8" size="2.8MB" validator="Hosp_03" time="1m ago" />
            <BlockCard index="1,247,890" txs="15" size="5.1MB" validator="Hosp_05" time="3m ago" />
            <BlockCard index="1,247,889" txs="10" size="3.4MB" validator="Hosp_01" time="4m ago" />
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-3">
            <Hash className="w-6 h-6 text-[#26C6DA]" /> Registration Stream
          </h3>
          <div className="glass-card overflow-hidden">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-white/5 text-[10px] font-black uppercase tracking-widest text-gray-500">
                  <th className="p-6">Tx Hash</th>
                  <th className="p-6">Entity</th>
                  <th className="p-6">Image ID</th>
                  <th className="p-6 text-right">Activity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <TxRow hash="0x3f8e...b2c4" entity="City Gen" id="CT-9912" time="2m" />
                <TxRow hash="0x9a2d...f5e1" entity="St. Mary's" id="MRI-4412" time="4m" />
                <TxRow hash="0x2c1f...d0a3" entity="Children's" id="XR-2210" time="7m" />
                <TxRow hash="0x7b68...ee14" entity="University" id="US-5511" time="12m" />
                <TxRow hash="0x1122...3344" entity="Private" id="PET-900" time="15m" />
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

const ExplorerStat = ({ label, value, icon: Icon }) => (
  <div className="glass-card p-6 border-b-2 border-transparent hover:border-[#7B68EE]/40 transition-all">
    <div className="flex justify-between items-start mb-4">
      <div className="w-10 h-10 bg-[#7B68EE]/10 rounded-xl flex items-center justify-center text-[#7B68EE]">
        <Icon className="w-5 h-5" />
      </div>
      <ArrowUpRight className="w-4 h-4 text-gray-700" />
    </div>
    <p className="text-[10px] font-black uppercase tracking-widest text-gray-500">{label}</p>
    <div className="text-2xl font-black mt-1">{value}</div>
  </div>
);

const BlockCard = ({ index, txs, size, validator, time }) => (
  <div className="glass-card p-6 flex items-center justify-between group cursor-pointer hover:translate-x-1 transition-transform border-l-4 border-l-transparent hover:border-l-[#7B68EE]">
    <div className="flex items-center gap-6">
      <div className="w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center font-black text-xs text-[#7B68EE]">
        BK
      </div>
      <div>
        <p className="font-black text-lg tracking-tight">#{index}</p>
        <div className="flex items-center gap-3 text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">
          <span>{txs} Transactions</span>
          <span className="w-1 h-1 bg-gray-700 rounded-full"></span>
          <span>{size}</span>
        </div>
      </div>
    </div>
    <div className="text-right">
      <p className="text-xs font-bold text-gray-400">Validator: <span className="text-[#7B68EE]">{validator}</span></p>
      <p className="text-[10px] text-gray-600 font-bold mt-1 uppercase">{time}</p>
    </div>
  </div>
);

const TxRow = ({ hash, entity, id, time }) => (
  <tr className="hover:bg-white/5 transition-colors cursor-pointer group">
    <td className="p-6 font-mono text-[#26C6DA] text-xs font-bold">{hash}</td>
    <td className="p-6 text-xs font-bold">{entity}</td>
    <td className="p-6 text-xs font-bold uppercase tracking-tighter">{id}</td>
    <td className="p-6 text-right">
      <span className="text-[10px] font-black text-gray-500 uppercase">{time} ago</span>
    </td>
  </tr>
);

export default Explorer;
