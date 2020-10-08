import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoCollection;

import org.bson.Document;
import java.util.Arrays;
import com.mongodb.Block;

import com.mongodb.client.MongoCursor;
import static com.mongodb.client.model.Filters.*;

public class mongo {
    public static void main( String args[] ) {
        //默认等于create("mongodb://hostOne:27017")
        MongoClient mongoClient = MongoClients.create();
        MongoDatabase database = mongoClient.getDatabase("test");
        MongoCollection<Document> student_col = database.getCollection("student");
        Document result = student_col.find().first();
        System.out.println(result.toJson());
        Document doc = new Document("name", "MongoDB")
                .append("type", "database")
                .append("count", 1)
                .append("versions", Arrays.asList("v3.2", "v3.0", "v2.6"))
                .append("info", new Document("x", 203).append("y", 102));
        student_col.insertOne(doc);
        Document birthdate= new Document("day",24)
                .append("month",7)
                .append("year",2000);

        String[] hobby={"football","basketball","reading"};
        Document doc2 = new Document("name","Chixinning")
                .append("gender","m")
                .append("birthdate",birthdate)
                .append("hobby",hobby)
                .append("city","Beijing");
        student_col.insertOne(doc2);

    }

}
