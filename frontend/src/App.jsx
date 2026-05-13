import { useState } from "react";

export default function App() {

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [sources, setSources] = useState([]);

  const generateContent = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      setResponse("");
      setSources([]);

      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_question: question,
        }),
      });

      const data = await res.json();

      setResponse(data.response);
      setSources(data.extracted_information || []);
    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white overflow-hidden">

      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-0 w-96 h-96 bg-pink-500 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-yellow-500 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-10">

        <nav className="flex items-center justify-between mb-16">
          <div>
            <h1 className="text-3xl font-black bg-gradient-to-r from-pink-500 to-yellow-500 bg-clip-text text-transparent">
              TrendForge AI
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Autonomous Research & Content Intelligence
            </p>
          </div>

          <button className="px-5 py-2 rounded-xl bg-white/10 border border-white/10 hover:bg-white/20 transition-all duration-300">
            Dashboard
          </button>
        </nav>

        <div className="grid lg:grid-cols-2 gap-10 items-center mb-16">

          <div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-6">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              <span className="text-sm text-slate-300">
                AI Research Engine Online
              </span>
            </div>

            <h2 className="text-6xl font-black leading-tight mb-6">
              Turn
              <span className="bg-gradient-to-r from-pink-500 to-yellow-500 bg-clip-text text-transparent">
                {" "}Web Noise{" "}
              </span>
              into Content Gold.
            </h2>

            <p className="text-slate-400 text-lg leading-relaxed max-w-xl">
              Discover trending insights, analyze multiple sources, and generate
              AI-powered content ideas using Tavily, LangGraph, and OpenAI.
            </p>

            <div className="flex gap-6 mt-10 flex-wrap">
              <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-4">
                <h3 className="text-3xl font-bold">3x</h3>
                <p className="text-slate-400 text-sm mt-1">
                  Faster Research
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-4">
                <h3 className="text-3xl font-bold">AI</h3>
                <p className="text-slate-400 text-sm mt-1">
                  Trend Synthesis
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-4">
                <h3 className="text-3xl font-bold">24/7</h3>
                <p className="text-slate-400 text-sm mt-1">
                  Autonomous Insights
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">

            <div className="mb-6">
              <h3 className="text-2xl font-bold mb-2">
                Research Topic
              </h3>
              <p className="text-slate-400 text-sm">
                Enter any trending topic for AI-powered content generation.
              </p>
            </div>

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Example: Latest trends in AI agents, Fintech AI startups, Future of autonomous systems..."
              rows={7}
              className="w-full bg-[#0f172a] border border-white/10 rounded-2xl p-5 outline-none focus:ring-2 focus:ring-pink-500 text-white resize-none"
            />

            <button
              onClick={generateContent}
              disabled={loading}
              className="w-full mt-6 py-4 rounded-2xl bg-gradient-to-r from-pink-500 to-yellow-500 text-black font-bold text-lg hover:scale-[1.01] transition-all duration-300 disabled:opacity-50"
            >
              {loading ? "Analyzing Web Intelligence..." : "Generate AI Content"}
            </button>

            <div className="grid grid-cols-3 gap-4 mt-8">
              <div className="bg-black/20 rounded-2xl p-4 border border-white/5">
                <p className="text-slate-400 text-sm">Sources</p>
                <h4 className="text-2xl font-bold">{sources.length}</h4>
              </div>

              <div className="bg-black/20 rounded-2xl p-4 border border-white/5">
                <p className="text-slate-400 text-sm">Pipeline</p>
                <h4 className="text-2xl font-bold">Live</h4>
              </div>

              <div className="bg-black/20 rounded-2xl p-4 border border-white/5">
                <p className="text-slate-400 text-sm">Agent</p>
                <h4 className="text-2xl font-bold">Active</h4>
              </div>
            </div>
          </div>
        </div>

        {response && (
          <div className="grid lg:grid-cols-3 gap-8 mt-10">

            <div className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-3xl font-black">
                    Generated Intelligence
                  </h2>
                  <p className="text-slate-400 mt-1">
                    Synthesized from multiple web sources.
                  </p>
                </div>

                <div className="px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm">
                  AI Generated
                </div>
              </div>

              <div className="bg-[#0f172a] rounded-2xl p-6 border border-white/5 max-h-[700px] overflow-y-auto">
                <pre className="whitespace-pre-wrap text-slate-200 leading-8 font-sans text-base">
                  {response}
                </pre>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 h-fit">
              <div className="mb-6">
                <h2 className="text-2xl font-black">
                  Research Sources
                </h2>
                <p className="text-slate-400 text-sm mt-1">
                  Tavily web intelligence pipeline.
                </p>
              </div>

              <div className="space-y-5 max-h-[700px] overflow-y-auto pr-2">
                {sources.map((source, index) => (
                  <div
                    key={index}
                    className="bg-[#0f172a] border border-white/5 rounded-2xl p-5 hover:border-pink-500/30 transition-all duration-300"
                  >
                    <div className="flex items-start justify-between gap-3 mb-3">
                      <h3 className="font-bold leading-6 text-white">
                        {source.title}
                      </h3>

                      <div className="min-w-fit text-xs px-2 py-1 rounded-full bg-pink-500/10 text-pink-400 border border-pink-500/20">
                        Source {index + 1}
                      </div>
                    </div>

                    <p className="text-slate-400 text-sm leading-6 line-clamp-6">
                      {source.content}
                    </p>

                    <a
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-2 mt-4 text-sm text-yellow-400 hover:text-yellow-300 transition-all"
                    >
                      Visit Source
                      <span>↗</span>
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-6 mt-20">

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 hover:-translate-y-1 transition-all duration-300">
            <div className="w-14 h-14 rounded-2xl bg-pink-500/10 flex items-center justify-center text-2xl mb-5">
              🔎
            </div>

            <h3 className="text-2xl font-bold mb-3">
              Real-Time Research
            </h3>

            <p className="text-slate-400 leading-7">
              Pull live web intelligence from Tavily and synthesize meaningful trends automatically.
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 hover:-translate-y-1 transition-all duration-300">
            <div className="w-14 h-14 rounded-2xl bg-yellow-500/10 flex items-center justify-center text-2xl mb-5">
              🧠
            </div>

            <h3 className="text-2xl font-bold mb-3">
              AI Synthesis
            </h3>

            <p className="text-slate-400 leading-7">
              Merge multiple information streams into one structured content strategy using LangGraph.
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 hover:-translate-y-1 transition-all duration-300">
            <div className="w-14 h-14 rounded-2xl bg-green-500/10 flex items-center justify-center text-2xl mb-5">
              ⚡
            </div>

            <h3 className="text-2xl font-bold mb-3">
              Content Pipeline
            </h3>

            <p className="text-slate-400 leading-7">
              Transform raw web data into newsletters, blogs, LinkedIn content, and research reports.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
