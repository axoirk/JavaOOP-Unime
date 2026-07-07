# Esercizio 1: Creazione Progetto con Maven

### Traccia
Usa il comando `mvn archetype:generate` da terminale per generare la struttura standard di un progetto Java con il file `pom.xml`.

### Esempio di Output
```text
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------< org.apache.maven:standalone-pom >-------------------
[INFO] Building Maven Stub Project (No POM) 1
[INFO] --------------------------------[ pom ]---------------------------------
...
[INFO] Generating project in Interactive mode
[INFO] No archetype defined. Using maven-archetype-quickstart (org.apache.maven.archetypes:maven-archetype-quickstart:1.4)
Define value for property 'groupId': org.example
Define value for property 'artifactId': my-app
Define value for property 'version' 1.0-SNAPSHOT: : 
Define value for property 'package' org.example: : 
Confirm properties configuration:
groupId: org.example
artifactId: my-app
version: 1.0-SNAPSHOT
package: org.example
 Y: : y
[INFO] ----------------------------------------------------------------------------
[INFO] Using following parameters for creating project from Archetype: maven-archetype-quickstart:1.4
[INFO] ----------------------------------------------------------------------------
[INFO] Parameter: groupId, Value: org.example
[INFO] Parameter: artifactId, Value: my-app
[INFO] Parameter: version, Value: 1.0-SNAPSHOT
[INFO] Parameter: package, Value: org.example
[INFO] Parameter: packageInPathFormat, Value: org/example
[INFO] Project created from Archetype in dir: /path/to/my-app
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

