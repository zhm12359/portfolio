/**
 * Calculate the detour distance between two different rides. 
 * Given four latitude / longitude pairs, where driver one 
 * is traveling from point A to point B and driver two is traveling 
 * from point C to point D, write a function 
 * (in your language of choice) to calculate the shorter of 
 * the detour distances the drivers would need to take to pick-up 
 * and drop-off the other driver.
 * 
 * ideas: if I didn't understand the question wrong, I should 
 * compare ACDB tour and CABD tour and find the min b/t them
 * b/c either AB or CD should in the middle for one driver to 
 * first pick the other up and then drop him off
 * putting these two paths in the middle can avoid a detour
 * for the driver on mission to the final destination
 * 
 * @author Hanming Zeng
 *
 */
public class CalcShort {
	
	public static void main(String[] args){
		
		//Assume we are given with four such points
		Point A = new Point(0,0);
		Point B = new Point(0,50);
		Point C = new Point(50,50);
		Point D = new Point(50,0);
		
		double AB = computeDis(A,B);
		double CD = computeDis(C,D);
		
		//since for ACDB and CABD, AC and BD are in common
		//so we just have to compare AB and CD
		
		if (AB > CD) {
	        System.out.println("Driver two should do it. ACDB is a shorter detour!");
	    } else if (AB == CD) {
	        System.out.println("ACDB is same as CABD. Both driver will make the same detour");
	    } else {
	        System.out.println("Driver one should do it. CABD is a shorter detour!!");
	    }
		

		
	}
	/**
	 * compute the distance b/t two points on earth
	 * using the formula I found online...
	 * @param p1
	 * @param p2
	 * @return
	 */
	public static double computeDis(Point p1, Point p2){
		
		double d1 = Math.toRadians((p2.getLongitude() - p1.getLongitude()));
		double d2 = Math.toRadians(p2.getLatitude() - p2.getLatitude());
		
		double a = Math.sin(d2/2) * Math.sin(d2/2) +
		        Math.cos(p1.getLatitude()) * Math.cos(p2.getLatitude()) *
		        Math.sin(d1/2) * Math.sin(d1/2);
		
		double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		
		double d = 637100 * c; //in meters
		
		return d;
			
	}
	
	
	

}
