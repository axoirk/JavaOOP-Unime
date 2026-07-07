# Esercizio 5: Build Automatica

### Traccia
Completa il ciclo di vita eseguendo `mvn clean install` o `mvn package` per impacchettare l'intera applicazione e le sue dipendenze in un file JAR o WAR distribuibile.

### Esempio di Output
```text
[INFO] Scanning for projects...
[INFO] 
[INFO] -----------------------< org.example:my-app >-----------------------
[INFO] Building my-app 1.0-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
...
[INFO] --- maven-jar-plugin:3.2.0:jar (default-jar) @ my-app ---
[INFO] Building jar: /path/to/my-app/target/my-app-1.0-SNAPSHOT.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.145 s
[INFO] Finished at: 2023-10-27T10:05:00Z
[INFO] ------------------------------------------------------------------------
```

