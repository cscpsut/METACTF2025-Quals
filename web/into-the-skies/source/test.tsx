
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Plane, Shield, Clock, MapPin, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface TicketData {
  passengerName: string;
  flightNumber: string;
  departure: string;
  arrival: string;
  gate: string;
  seat: string;
  boardingTime: string;
  departureTime: string;
  securityCode: string;
  ticketNumber: string;
  profileImageUrl: string;
}

const TicketForm = () => {
  const { toast } = useToast();
  const [isGenerating, setIsGenerating] = useState(false);
  const [ticketData, setTicketData] = useState<TicketData>({
    passengerName: '',
    flightNumber: '',
    departure: '',
    arrival: '',
    gate: '',
    seat: '',
    boardingTime: '',
    departureTime: '',
    securityCode: '',
    ticketNumber: '',
    profileImageUrl: ''
  });

  const generateTicketHTML = (data: TicketData) => {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Courier New', monospace; 
                background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
                padding: 20px;
                color: #1f2937;
            }
            .ticket {
                background: white;
                width: 800px;
                margin: 0 auto;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            }
            .header {
                background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%);
                color: white;
                padding: 20px;
                text-align: center;
                position: relative;
            }
            .security-badge {
                position: absolute;
                top: 10px;
                right: 20px;
                background: rgba(255, 255, 255, 0.2);
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            .main-content {
                padding: 30px;
                background: #f8fafc;
            }
            .passenger-section {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 30px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .profile-image {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #dc2626;
                background: #f3f4f6;
            }
            .passenger-info {
                flex: 1;
            }
            .passenger-name {
                font-size: 24px;
                font-weight: bold;
                color: #1f2937;
                margin-bottom: 5px;
            }
            .passenger-label {
                font-size: 12px;
                color: #6b7280;
                text-transform: uppercase;
            }
            .flight-info {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .route {
                display: flex;
                align-items: center;
                gap: 20px;
                font-size: 24px;
                font-weight: bold;
            }
            .arrow {
                color: #3b82f6;
                font-size: 30px;
            }
            .details-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            .detail-box {
                background: white;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #dc2626;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .detail-label {
                font-size: 12px;
                color: #6b7280;
                text-transform: uppercase;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .detail-value {
                font-size: 16px;
                font-weight: bold;
                color: #1f2937;
            }
            .barcode-section {
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .barcode {
                font-family: 'Courier New', monospace;
                font-size: 24px;
                letter-spacing: 2px;
                background: #000;
                color: white;
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .security-notice {
                background: #fef2f2;
                border: 2px solid #fca5a5;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
                color: #991b1b;
                font-weight: bold;
            }
            .timestamp {
                position: absolute;
                bottom: 10px;
                right: 20px;
                font-size: 10px;
                color: rgba(255, 255, 255, 0.8);
            }
        </style>
    </head>
    <body>
        <div class="ticket">
            <div class="header">
                <div class="security-badge"> SECURE</div>
                <h1>BOARDING PASS</h1>
                <h2>SECURITY VERIFIED</h2>
                <div class="timestamp">Generated: ${new Date().toLocaleString()}</div>
            </div>
            
            <div class="main-content">
                <div class="passenger-section">
                    ${data.profileImageUrl
  ? `<iframe src="${data.profileImageUrl}"
             class="profile-image"
             style="width:100% !important; height:100% !important; border-radius:0 !important; border:1px solid #ccc;"></iframe>
     ></iframe>`
  : '<div class="profile-image" style="display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:24px;"></div>'}
                    <div class="passenger-info">
                        <div class="passenger-name">${data.passengerName}</div>
                        <div class="passenger-label">Passenger Name</div>
                    </div>
                </div>
                
                <div class="flight-info">
                    <div class="route">
                        <span>${data.departure}</span>
                        <span class="arrow">→</span>
                        <span>${data.arrival}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 20px; font-weight: bold; color: #dc2626;">${data.flightNumber}</div>
                        <div style="font-size: 14px; color: #6b7280;">Flight Number</div>
                    </div>
                </div>
                
                <div class="details-grid">
                    <div class="detail-box">
                        <div class="detail-label">Seat</div>
                        <div class="detail-value">${data.seat}</div>
                    </div>
                    <div class="detail-box">
                        <div class="detail-label">Gate</div>
                        <div class="detail-value">${data.gate}</div>
                    </div>
                    <div class="detail-box">
                        <div class="detail-label">Boarding Time</div>
                        <div class="detail-value">${data.boardingTime}</div>
                    </div>
                    <div class="detail-box">
                        <div class="detail-label">Departure Time</div>
                        <div class="detail-value">${data.departureTime}</div>
                    </div>
                    <div class="detail-box">
                        <div class="detail-label">Security Code</div>
                        <div class="detail-value">${data.securityCode}</div>
                    </div>
                </div>
                
                <div class="barcode-section">
                    <div style="font-size: 14px; color: #6b7280; margin-bottom: 10px;">TICKET NUMBER</div>
                    <div class="barcode">${data.ticketNumber}</div>
                    <div style="font-size: 12px; color: #6b7280; margin-top: 10px;">Scan at security checkpoint</div>
                </div>
                
                <div class="security-notice">
                    SECURITY NOTICE: Present this boarding pass and valid ID at security checkpoint.
                    Arrive at gate 30 minutes before boarding time. Subject to security screening.
                </div>
            </div>
        </div>
    </body>
    </html>`;
  };

  const handleInputChange = (field: keyof TicketData, value: string) => {
    setTicketData(prev => ({ ...prev, [field]: value }));
  };

  const generateRandomData = () => {
    const airports = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'SEA', 'LAS', 'PHX'];
    const airlines = ['AA', 'UA', 'DL', 'WN', 'AS', 'B6'];
    
    setTicketData({
      passengerName: 'JOHN DOE',
      flightNumber: `${airlines[Math.floor(Math.random() * airlines.length)]}${Math.floor(Math.random() * 9000) + 1000}`,
      departure: airports[Math.floor(Math.random() * airports.length)],
      arrival: airports[Math.floor(Math.random() * airports.length)],
      gate: `${String.fromCharCode(65 + Math.floor(Math.random() * 26))}${Math.floor(Math.random() * 50) + 1}`,
      seat: `${Math.floor(Math.random() * 30) + 1}${String.fromCharCode(65 + Math.floor(Math.random() * 6))}`,
      boardingTime: '14:30',
      departureTime: '15:00',
      securityCode: Math.random().toString(36).substring(2, 8).toUpperCase(),
      ticketNumber: Math.random().toString().substring(2, 15),
      profileImageUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
    });
  };

  const generatePDF = async () => {
    if (!ticketData.passengerName || !ticketData.flightNumber) {
      toast({
        title: "Missing Information",
        description: "Please fill in at least passenger name and flight number.",
        variant: "destructive"
      });
      return;
    }

    setIsGenerating(true);
    
    try {
      const htmlContent = generateTicketHTML(ticketData);
      
      const response = await fetch('http://localhost:80/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `html=${encodeURIComponent(htmlContent)}`
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `boarding-pass-${ticketData.flightNumber}-${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        toast({
          title: "PDF Generated Successfully",
          description: "Your boarding pass has been downloaded.",
        });
      } else {
        throw new Error('Failed to generate PDF');
      }
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: "Could not generate PDF. Please check your backend connection.",
        variant: "destructive"
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader className="bg-gradient-to-r from-blue-900 to-indigo-900 text-white">
        <CardTitle className="flex items-center gap-3 text-2xl">
          <Shield className="h-8 w-8" />
          Airport Security - Boarding Pass Generator
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Plane className="h-5 w-5" />
            Flight Information
          </h3>
          <Button 
            onClick={generateRandomData}
            variant="outline"
            className="text-sm"
          >
            Generate Sample Data
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="passengerName">Passenger Name</Label>
            <Input
              id="passengerName"
              value={ticketData.passengerName}
              onChange={(e) => handleInputChange('passengerName', e.target.value)}
              placeholder="JOHN DOE"
              className="font-mono"
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="profileImageUrl" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Profile Image URL
            </Label>
            <Input
              id="profileImageUrl"
              value={ticketData.profileImageUrl}
              onChange={(e) => handleInputChange('profileImageUrl', e.target.value)}
              placeholder="https://example.com/profile-image.jpg"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="flightNumber">Flight Number</Label>
            <Input
              id="flightNumber"
              value={ticketData.flightNumber}
              onChange={(e) => handleInputChange('flightNumber', e.target.value)}
              placeholder="AA1234"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="departure">Departure</Label>
            <Input
              id="departure"
              value={ticketData.departure}
              onChange={(e) => handleInputChange('departure', e.target.value)}
              placeholder="JFK"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="arrival">Arrival</Label>
            <Input
              id="arrival"
              value={ticketData.arrival}
              onChange={(e) => handleInputChange('arrival', e.target.value)}
              placeholder="LAX"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="gate">Gate</Label>
            <Input
              id="gate"
              value={ticketData.gate}
              onChange={(e) => handleInputChange('gate', e.target.value)}
              placeholder="A15"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="seat">Seat</Label>
            <Input
              id="seat"
              value={ticketData.seat}
              onChange={(e) => handleInputChange('seat', e.target.value)}
              placeholder="12A"
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="boardingTime">Boarding Time</Label>
            <Input
              id="boardingTime"
              type="time"
              value={ticketData.boardingTime}
              onChange={(e) => handleInputChange('boardingTime', e.target.value)}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="departureTime">Departure Time</Label>
            <Input
              id="departureTime"
              type="time"
              value={ticketData.departureTime}
              onChange={(e) => handleInputChange('departureTime', e.target.value)}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="securityCode">Security Code</Label>
            <Input
              id="securityCode"
              value={ticketData.securityCode}
              onChange={(e) => handleInputChange('securityCode', e.target.value)}
              placeholder="SEC123"
              className="font-mono"
            />
          </div>

          <div className="space-y-2 md:col-span-2 lg:col-span-3">
            <Label htmlFor="ticketNumber">Ticket Number</Label>
            <Input
              id="ticketNumber"
              value={ticketData.ticketNumber}
              onChange={(e) => handleInputChange('ticketNumber', e.target.value)}
              placeholder="1234567890123"
              className="font-mono"
            />
          </div>
        </div>

        <Separator />

        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="h-4 w-4" />
            <span>PDF will be generated and downloaded automatically</span>
          </div>
          
          <Button 
            onClick={generatePDF}
            disabled={isGenerating}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold px-8 py-2"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating...
              </>
            ) : (
              <>
                <Shield className="h-4 w-4 mr-2" />
                Generate Secure PDF
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TicketForm;