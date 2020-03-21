scalaVersion := "2.12.4"

// Note, it's not required for you to define these three settings. These are
// mostly only necessary if you intend to publish your library's binaries on a
// place like Sonatype or Bintray.
name := "HelloLucene"
organization := "name.kitazaki.scala"
version := "1.0"

val luceneVersion = "7.2.1"

// https://mvnrepository.com/artifact/org.apache.lucene/
libraryDependencies ++= Seq(
    "org.apache.lucene" % "lucene-core" % luceneVersion,
    "org.apache.lucene" % "lucene-analyzers-common" % luceneVersion,
    "org.apache.lucene" % "lucene-queryparser" % luceneVersion,
    "org.apache.lucene" % "lucene-queries" % luceneVersion,
    "org.apache.lucene" % "lucene-test-framework" % luceneVersion
)
