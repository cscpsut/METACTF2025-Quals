import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Shield, ArrowRight, Plane } from "lucide-react";

const Index = () => {
  const [isProcessing, setIsProcessing] = useState(false);

  const handleRedirect = () => {
    setIsProcessing(true);

    setTimeout(() => {
      window.location.href = "https://skpwpxx6n1.execute-api.us-east-1.amazonaws.com/"; 
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 text-6xl rotate-12">
          <Plane className="text-blue-300" />
        </div>
        <div className="absolute bottom-20 right-20 text-8xl -rotate-12">
          <Shield className="text-blue-400" />
        </div>
        <div className="absolute top-1/2 left-1/4 text-4xl rotate-45">
          <Shield className="text-blue-200" />
        </div>
      </div>

      {/* Top Shield Icon */}
      <div className="relative z-10 mb-8">
        <Shield className="w-24 h-24 text-blue-300" />
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center max-w-2xl mx-auto px-6">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center justify-center mb-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white tracking-wide">
              SECURITY CHECKPOINT
            </h1>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-6 mb-8">
            <p className="text-xl text-blue-100 mb-2">
              Welcome to Skyway Security Portal
            </p>
            <p className="text-blue-200/80 text-sm">
              Please proceed to the authorized access point
            </p>
          </div>
        </div>

        {/* Security Badge */}
        <div className="bg-white rounded-lg p-6 shadow-2xl mb-8 border-l-4 border-blue-600">
          <div className="flex items-center justify-center mb-4">
            <div className="bg-blue-600 p-2 rounded-full mr-3">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="text-slate-800 font-semibold text-lg">AUTHORIZED ACCESS</span>
          </div>
          <div className="text-slate-600 text-sm">
            Security Level: RESTRICTED
          </div>
        </div>

        {/* Redirect Button */}
        <div className="space-y-4">
          <Button
            onClick={handleRedirect}
            disabled={isProcessing}
            className={`
              w-full py-6 text-lg font-semibold tracking-wide transition-all duration-300
              ${isProcessing 
                ? 'bg-amber-600 hover:bg-amber-600' 
                : 'bg-blue-600 hover:bg-blue-700 hover:scale-105'
              }
              text-white shadow-xl hover:shadow-2xl
              border-2 border-blue-400/30
            `}
          >
            {isProcessing ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                PROCESSING SECURITY CLEARANCE...
              </div>
            ) : (
              <div className="flex items-center justify-center">
                <Shield className="w-6 h-6 mr-3" />
                PROCEED TO SECURE AREA
                <ArrowRight className="w-6 h-6 ml-3" />
              </div>
            )}
          </Button>
          
          <p className="text-blue-200/60 text-xs">
            Click to access the authorized endpoint
          </p>
        </div>

        {/* Status Indicator */}
        <div className="mt-8 flex items-center justify-center space-x-4 text-sm">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></div>
            <span className="text-green-300">SYSTEM ONLINE</span>
          </div>
          <div className="w-px h-4 bg-white/20"></div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-400 rounded-full mr-2"></div>
            <span className="text-blue-300">SECURITY ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Bottom Security Strip */}
      <div className="absolute bottom-0 left-0 right-0 bg-blue-600/20 backdrop-blur-sm border-t border-blue-400/30 py-3">
        <div className="text-center text-blue-200/80 text-xs tracking-wider">
          SKYWAY SECURITY SYSTEMS • AUTHORIZED PERSONNEL ONLY • EST. 2025
        </div>
      </div>
    </div>
  );
};

export default Index;
