import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Crown, Loader2 } from 'lucide-react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file || !jd) return alert("Please provide both documents.");
    setLoading(true);
    const formData = new FormData();
    formData.append("resume_file", file);
    formData.append("jd_text", jd);

    try {
      const response = await axios.post("http://127.0.0.1:8000/scan", formData);
      setResult(response.data.data);
    } catch (error) {
      alert("System connection error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="dynamic-bg">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>

      <div className="min-h-screen text-slate-200 font-serif relative z-10">
        <nav className="p-8 flex justify-between items-center bg-black/40 backdrop-blur-xl border-b border-yellow-600/20">
          <div className="flex items-center gap-3 font-bold text-2xl tracking-tighter text-yellow-600">
            <Crown size={32} /> <span>PRESTIGE ATS</span>
          </div>
        </nav>

        <main className="max-w-6xl mx-auto py-16 px-6">
          <header className="text-center mb-16">
            <h1 className="text-6xl font-black mb-6 text-white tracking-tight italic">
              Elevate Your <span className="text-yellow-600">Standard</span>
            </h1>
            <p className="text-slate-400 text-xl max-w-2xl mx-auto font-light tracking-wide">
              Professional Grade Resume Intelligence for the Discerning Candidate.
            </p>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Input Section */}
            <div className="glass-card p-10 rounded-none border-t-4 border-t-yellow-600">
              <div className="space-y-8">
                <div>
                  <label className="text-xs uppercase tracking-widest text-yellow-600 font-bold mb-3 block">Requirement Specs</label>
                  <textarea 
                    className="w-full h-48 p-5 bg-black/40 border border-white/10 rounded-none text-white focus:border-yellow-600 transition-all outline-none"
                    value={jd}
                    onChange={(e) => setJd(e.target.value)}
                  />
                </div>

                <div className="border border-white/10 p-10 text-center hover:bg-white/5 transition-all">
                  <input type="file" className="hidden" id="resumeInput" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
                  <label htmlFor="resumeInput" className="cursor-pointer">
                    <Upload className="mx-auto text-yellow-600 mb-4" />
                    <p className="text-slate-300 uppercase text-xs tracking-widest">{file ? file.name : "Upload Document"}</p>
                  </label>
                </div>

                <button onClick={handleUpload} disabled={loading} className="w-full py-5 bg-yellow-600 hover:bg-yellow-700 text-black font-black uppercase tracking-widest transition-all">
                  {loading ? <Loader2 className="animate-spin mx-auto" /> : "Initiate Audit"}
                </button>
              </div>
            </div>

            {/* Result Section */}
            <div className="glass-card p-10 rounded-none flex flex-col items-center justify-center relative overflow-hidden">
              {!result ? (
                <div className="text-center py-20">
                  <p className="text-slate-600 italic tracking-widest uppercase text-sm">System Ready for Input</p>
                </div>
              ) : (
                <div className="w-full space-y-12 animate-in fade-in zoom-in duration-1000">
                  <div className="text-center">
                    <h2 className="text-9xl font-black text-white leading-none">{result.final_score}</h2>
                    <p className="text-yellow-600 font-bold tracking-[.5em] uppercase text-xs mt-4">Match Efficiency</p>
                  </div>
                  
                  <div className="grid grid-cols-1 gap-6">
                    <div className="p-6 bg-white/5 border border-yellow-600/20">
                      <h3 className="text-yellow-600 text-[10px] font-bold uppercase tracking-widest mb-4">Acquired Assets</h3>
                      <div className="flex flex-wrap gap-3">
                        {result.matched_keywords.map((word, i) => (
                          <span key={i} className="text-[10px] text-white border border-white/20 px-3 py-1 uppercase">{word}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}

export default App;