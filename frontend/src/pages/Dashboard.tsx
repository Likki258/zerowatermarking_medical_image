import React from 'react';
import { Activity, ShieldCheck, AlertCircle, HardDriveIndicator } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: '08:00', value: 12 },
  { name: '10:00', value: 18 },
  { name: '12:00', value: 15 },
  { name: '14:00', value: 24 },
  { name: '16:00', value: 20 },
  { name: '18:00', value: 28 },
];

const Dashboard = () => {
  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">Hospital <span className="text-[#4A90E2]">Dashboard</span></h1>
          <p className="text-gray-400">Welcome back, City General. Monitoring institutional medical provenance.</p>
        </div>
        <div className="text-right hidden sm:block">
          <p className="text-xs text-gray-500 uppercase font-black tracking-widest mb-1">Network Health</p>
          <div className="flex gap-1 justify-end">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="w-4 h-1.5 bg-green-500 rounded-full"></div>
            ))}
          </div>
        </div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="Images Registered" value="1,248" icon={Activity} trend="+12%" />
        <StatCard label="Verified Authenticity" value="99.9%" icon={ShieldCheck} trend="Stable" />
        <StatCard label="Pending Alerts" value="2" icon={AlertCircle} trend="Action" color="text-red-500" />
        <StatCard label="Node Status" value="Online" icon={HardDriveIndicator} trend="47/48" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Activity Chart */}
        <div className="lg:col-span-2 glass-card p-8">
          <h3 className="text-xl font-bold mb-8">Registration Activity</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" />
                <XAxis dataKey="name" stroke="#666" fontSize={12} />
                <YAxis stroke="#666" fontSize={12} />
                <Tooltip 
                  contentStyle={{ background: '#111', border: '1px solid #333', borderRadius: '8px' }}
                />
                <Line type="monotone" dataKey="value" stroke="#4A90E2" strokeWidth={3} dot={{ r: 4, fill: '#4A90E2' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alert Summary */}
        <div className="glass-card p-8">
          <h3 className="text-xl font-bold mb-8">Latest Transactions</h3>
          <div className="space-y-6">
            <TransactionItem id="#TX-8821" type="Chest X-Ray" status="Success" time="2m ago" />
            <TransactionItem id="#TX-8820" type="Brain MRI" status="Success" time="15m ago" />
            <TransactionItem id="#TX-8819" type="Knee X-Ray" status="Pending" time="1h ago" />
            <TransactionItem id="#TX-8818" type="Chest CT" status="Success" time="3h ago" />
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, trend, color = "text-[#4A90E2]" }) => (
  <div className="glass-card p-6 flex items-center gap-6">
    <div className={`p-4 bg-white/5 rounded-2xl ${color}`}>
      <Icon className="w-8 h-8" />
    </div>
    <div>
      <p className="text-xs text-gray-500 font-bold uppercase tracking-widest">{label}</p>
      <div className="text-2xl font-black mt-1">{value}</div>
      <p className="text-[10px] text-gray-400 mt-1 uppercase font-bold">{trend}</p>
    </div>
  </div>
);

const TransactionItem = ({ id, type, status, time }) => (
  <div className="flex items-center justify-between group cursor-pointer hover:bg-white/5 p-2 -m-2 rounded-xl transition-colors">
    <div className="flex items-center gap-4">
      <div className={`w-2 h-2 rounded-full ${status === 'Success' ? 'bg-green-500' : 'bg-orange-500'}`}></div>
      <div>
        <p className="text-sm font-bold">{type}</p>
        <p className="text-[10px] text-gray-500 font-bold tracking-widest">{id}</p>
      </div>
    </div>
    <div className="text-right">
      <p className="text-xs font-bold text-gray-400">{time}</p>
    </div>
  </div>
);

export default Dashboard;
