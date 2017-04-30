package NoiseUDP;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetSocketAddress;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

public class NoiseUDP 
{
	private static final Integer MTU = 1492;	// Let it be fixed for now.
	
	private static Integer port;	// 1024->65535
    private static Integer size;	// 0->(MTU-52)
    private static Double interval;	// 1.0->1000.0
    
	public static void main(String argv[]) throws IOException, InterruptedException
    {    
		if(argv.length > 0)
		{
			port = Integer.parseInt(argv[0]);
			if (port < 1024)
				port = 1024;
			else if (port > 65535)
				port = 65535;

        	if(argv.length > 1)
        	{
				size = Integer.parseInt(argv[1]);
				if (size < 0)
					size = 0;
				else if (size > MTU - 52)
					size = MTU - 52;
					
				if(argv.length > 2)
				{
					interval = Double.parseDouble(argv[2]);
					if (interval < 1.0)
						interval = 1.0;
					else if (interval > 1000.0)
						interval = 1000.0;
				}
				else
					interval = 1.0;
			}
			else
				size = 1440;
		}
		else
			port = 65535;

        Thread t = new Thread(new Runnable()
        {
    		public void run()
			{
    			DatagramSocket serverSocket = null;
    			try
				{
					serverSocket = new DatagramSocket();
					serverSocket.setBroadcast(true);
					InetSocketAddress address = new InetSocketAddress("255.255.255.255", port);
					byte[] sendData = new byte[size];
					Arrays.fill(sendData, (byte)0xFF);	// Set all bits to 1
					System.out.println("Payload: " + sendData.length);
					long milli = interval.longValue();
					System.out.println("Milliseconds: " + milli);
					int nano = (int)((interval - milli) * 1000000.0);
					System.out.println("Nanoseconds: " + nano);
					DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, address);
					System.out.println("Calculated Data Rate: " + ((sendData.length + 52) * 8.0) / ((double)milli / 1000.0 + (double)nano / 1000000.0) + " Bit/s");
					while(true)
					{
						serverSocket.send(sendPacket);
						Thread.sleep(milli, nano);
					}
				}
				catch (Exception ex)
				{
					Logger.getLogger(NoiseUDP.class.getName()).log(Level.SEVERE, null, ex);
				}
				finally
				{
					if(serverSocket != null && !serverSocket.isClosed())
						serverSocket.close();
				}
			}
        });
        t.start();
        t.join();
        System.exit(0);
	}
}
