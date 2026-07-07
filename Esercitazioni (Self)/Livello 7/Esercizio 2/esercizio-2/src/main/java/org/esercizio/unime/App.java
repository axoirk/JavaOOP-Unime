package org.esercizio.unime;


import javax.xml.transform.Result;
import java.sql.*;


public class App
{
    public static void main( String[] args )
    {
        String db_url = "jdbc:mysql://localhost:3306/test_db";

        System.out.println("Connecting to database...");
        try (Connection conn = DriverManager.getConnection(db_url, "root", "admin1234")) {
            System.out.println("Connection successful!");
            System.out.println("Executing test query: SELECT 1");
            PreparedStatement query = conn.prepareStatement("SELECT 1");

            try(ResultSet rs = query.executeQuery()) {
                if (rs.next()) {
                    int result = rs.getInt(1);
                    System.out.println("Result: " + result);
                } else {
                    System.out.println("Nessun risultato trovato.");
                }
            }

            System.out.println("Closing connection.");
            conn.close();

        } catch (SQLException e) {
            System.out.println("Error during interacting: " + e.getMessage());;
        }
    }
}
