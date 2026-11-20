import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[KhetSathi ErrorBoundary] Uncaught runtime error:', error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-[#f4f7f4] p-4 text-[#0f1f17]">
          <div className="max-w-md w-full bg-white rounded-3xl p-6 shadow-xl border border-emerald-200 text-center space-y-4">
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto text-3xl">
              🌾
            </div>
            
            <div className="space-y-1">
              <h2 className="text-xl font-black text-emerald-950">
                KhetSathi 360
              </h2>
              <p className="text-sm font-bold text-slate-700">
                पृष्ठ लोड करने में समस्या आई / Application Error
              </p>
              <p className="text-xs text-slate-500">
                सर्वर या नेटवर्क प्रतिक्रिया में अस्थायी रुकावट आई है।
              </p>
            </div>

            {this.state.error && (
              <div className="p-3 bg-red-50 rounded-xl text-left border border-red-200 text-xs font-mono text-red-800 overflow-x-auto max-h-32">
                {this.state.error.message}
              </div>
            )}

            <div className="pt-2 flex flex-col gap-2.5">
              <button
                type="button"
                onClick={this.handleReload}
                className="w-full py-3 px-4 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm rounded-xl shadow-md transition cursor-pointer"
              >
                🔄 पृष्ठ पुनः लोड करें / Refresh Page
              </button>

              <a
                href="/legacy"
                className="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs rounded-xl border border-slate-300 transition text-center block"
              >
                🌾 सुरक्षित क्लासिक संस्करण खोलें (Safe Classic /legacy)
              </a>
            </div>

            <p className="text-[11px] text-slate-400">
              National Digital Agriculture Decision System · 24x7 Offline Resilient
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
