<?php

class SqlConnector {

    //init
    protected $verbindung;
    protected $mysql_host = $GLOBALS["conf"]["mysql"]["host"];
    protected $mysql_user = $GLOBALS["conf"]["mysql"]["user"];
    protected $mysql_passwort = $GLOBALS["conf"]["mysql"]["password"];
    protected $mysql_db = $GLOBALS["conf"]["mysql"]["database"];
    
    public function __construct($live = false) {

            $this->verbindung = new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_passwort, $this->mysql_db) or echo "TODO: return an error";

    }

    public function __destruct() {
        $this->verbindung->close();
    }
    
    public function getLastError(){
        return $this->verbindung->error;
    }

    public function query($str, $unicode = true) {
        if ($unicode) {
            $this->verbindung->query("SET CHARACTER SET utf8");
        } else {
            $this->verbindung->query("SET CHARACTER SET latin1");
        }
        return $this->verbindung->query($str);
    }

    public function esc($str) {
        return $this->verbindung->escape_string($str);
    }
    
    public function saveAnalysisResult($input, $output){
        if (!($stmt = $this->db->prepare("INSERT INTO results (input, output) VALUES(?, ?)"))) echo "TODO: return an error";
        $stmt->bind("ss",$input,$output);
        $stmt->execute();
    }

}
