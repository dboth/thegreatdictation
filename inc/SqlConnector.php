<?php

require_once __DIR__."/config.php";

class SqlConnector {

    //init
     protected $verbindung, $mysql_host, $mysql_user, $mysql_passwort, $mysql_db;

    public function __construct($live = false) {
        $this->mysql_host = $GLOBALS["conf"]["mysql"]["host"];
        $this->mysql_user = $GLOBALS["conf"]["mysql"]["user"];
        $this->mysql_passwort = $GLOBALS["conf"]["mysql"]["password"];
        $this->mysql_db = $GLOBALS["conf"]["mysql"]["database"];
        $this->verbindung = @new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_passwort, $this->mysql_db);
        if ($this->verbindung->connect_error) {
            die('Connect Error: ' . $this->verbindung->connect_error);
        }
    }

    public function __destruct() {
        if (!$this->verbindung->connect_error) 
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
        if (!($stmt = $this->verbindung->prepare("INSERT INTO results_v0 (input, output) VALUES(?, ?)"))) die("TODO: return an error");
        $stmt->bind_param("ss",$input,$output);
        $stmt->execute();
    }

    public function saveFeedback($title, $subject, $text){
        //feedback table sollte dann auch eine time spalte haben, die automatisch den timestamp erhält
        if (!($stmt = $this->verbindung->prepare("INSERT INTO feedback (title, subject, text) VALUES(?, ?, ?)"))) {
            die("TODO: return an error");
            return false;
            }
        $stmt->bind_param("sss",$title, $subject, $text);
        $stmt->execute();
        return true;
    }

}
