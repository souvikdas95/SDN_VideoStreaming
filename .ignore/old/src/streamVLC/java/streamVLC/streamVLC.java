package streamVLC;

import uk.co.caprica.vlcj.player.MediaPlayer;
import uk.co.caprica.vlcj.player.MediaPlayerFactory;
import uk.co.caprica.vlcj.discovery.NativeDiscovery;

public class streamVLC
{
	// public static int spinCount = 0;
	public static MediaPlayer player;
	public static String options;
	public static String ip;
	public static int port;
	public static String mrl;
	
	public static void main(String[] argv) throws Exception
    {
		new NativeDiscovery().discover();
    	ip = argv[0];
    	port = Integer.parseInt(argv[1]);
    	// options = formatRtspStream(ip, port, "demo");
    	options = formatRtpStream(ip, port);
    	mrl = argv[2];
        System.out.println("Streaming '" + mrl + "' to 'rtp://@" + ip + ":" + port + "'\n(" + options + ")");
        MediaPlayerFactory factory = new MediaPlayerFactory();
        player = factory.newHeadlessMediaPlayer();
        Thread.sleep(1000);
        Thread t = new Thread(new Runnable()
        {
        	public void run()
        	{
        		player.startMedia
        		(
    				mrl,
    	            options,
    	            ":no-sout-rtp-sap",
    	            ":no-sout-standard-sap",
    	            ":sout-all",
    	            ":sout-keep"
	            );
        	}
        });
    	t.start();
    	while(!t.isAlive());
    	Thread.sleep(1000);
    	while(player.isPlaying())
    	{
    		System.out.println(player.getTime() + "/" + player.getLength());
    		Thread.sleep(1000);
    	}
    	if(t.isAlive())
    		t.interrupt();
    	System.exit(0);
    }

    /*private static String formatRtspStream(String serverAddress, int serverPort, String id)
    {
        StringBuilder sb = new StringBuilder(60);
        sb.append(":sout=#rtp{sdp=rtsp://");
        sb.append(serverAddress);
        sb.append(':');
        sb.append(serverPort);
        sb.append('/');
        sb.append(id);
        sb.append("}");
        return sb.toString();
    }*/

    private static String formatRtpStream(String serverAddress, int serverPort)
    {
        StringBuilder sb = new StringBuilder(60);
        sb.append(":sout=#rtp{dst=");
        sb.append(serverAddress);
        sb.append(",port=");
        sb.append(serverPort);
        sb.append(",mux=ts}");
        return sb.toString();
    }
}
