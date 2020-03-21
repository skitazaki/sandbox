import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;

object Main extends App {
  println("Hello, Lucene " + Version.LATEST + "!")

  val analyzer = new StandardAnalyzer

  // 1. create the index
  val index = new RAMDirectory
  val config = new IndexWriterConfig(analyzer)
  val w = new IndexWriter(index, config)
  addDoc(w, "Lucene in Action", "193398817")
  addDoc(w, "Lucene for Dummies", "55320055Z")
  addDoc(w, "Managing Gigabytes", "55063554A")
  addDoc(w, "The Art of Computer Science", "9900333X")
  w.close

  // 2. query
  val querystr = if (args.length > 0) args(0) else "lucene"
  val q = new QueryParser("title", analyzer).parse(querystr)

  // 3. search
  val hitsPerPage = 10
  val reader = DirectoryReader.open(index)
  val searcher = new IndexSearcher(reader)
  val collector = TopScoreDocCollector.create(hitsPerPage)
  searcher.search(q, collector)
  val hits = collector.topDocs.scoreDocs

  // 4. display results
  println("Found " + hits.length + " hits.")
  hits.foreach { r =>
    val d = searcher.doc(r.doc)
    println(d.get("isbn") + "\t" + d.get("title") + "\t" + r.score)
  }
  reader.close

  def addDoc(w : IndexWriter, title : String, isbn : String) = {
    val doc = new Document
    doc.add(new TextField("title", title, Field.Store.YES))
    // use a string field for isbn because we don't want it tokenized
    doc.add(new StringField("isbn", isbn, Field.Store.YES))
    w.addDocument(doc)
  }
}
