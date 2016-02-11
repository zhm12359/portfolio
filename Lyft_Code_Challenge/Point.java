/**
 * Points that contain longitude and latitude information;
 * @author zenghanming
 *
 */
public class Point {
	
	
		private double latitude;
		private double longitude;
		
		public Point(double lati, double longi){

			latitude = lati;
			longitude = longi;
		}
		
		public double getLatitude() {
			return latitude;
		}

		public void setLatitude(double x) {
			this.latitude = x;
		}

		public double getLongitude() {
			return longitude;
		}

		public void setLongitude(double y) {
			this.longitude = y;
		}
	

}
