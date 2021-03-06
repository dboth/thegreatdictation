<?php

require_once __DIR__."/config.php";
require_once __DIR__."/ErrorHandler.php";

class SqlConnector {

    //init
    protected $verbindung, $mysql_host, $mysql_user, $mysql_passwort, $mysql_db;

    public function __construct($live = false) {
        $this->errors = new ErrorHandler(__CLASS__);
        $this->mysql_host = $GLOBALS["conf"]["mysql"]["host"];
        $this->mysql_user = $GLOBALS["conf"]["mysql"]["user"];
        $this->mysql_passwort = $GLOBALS["conf"]["mysql"]["password"];
        $this->mysql_db = $GLOBALS["conf"]["mysql"]["database"];
        $this->verbindung = @new mysqli($this->mysql_host, $this->mysql_user, $this->mysql_passwort, $this->mysql_db);
        if ($this->verbindung->connect_error) {
            die($this->errors->createErrorJSON("b_db_connection_error", $this->verbindung->connect_error));
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

    public function saveAnalysisResult($input, $output, $username = ""){
        $output_arr = json_decode($output, true);
        if ($output_arr){
            $text_id = $output_arr["0"]["data"]["text_id"];
            $score1 = $output_arr["0"]["data"]["score"][0];
            $score2 = $output_arr["0"]["data"]["score"][1];
            $score3 = $output_arr["0"]["data"]["score"][2];
        } else {
            $text_id = 0;
            $score1 = 0;
            $score2 = 0;
            $score3 = 0;
        }
        if (!($stmt = $this->verbindung->prepare("INSERT INTO results_v0 (input, output, username, text_id, score, correct_words, total_words) VALUES(?, ?, ?, ?, ?, ? ,?)"))) die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "results_v0"));
        $stmt->bind_param("sssssss",$input,$output, $username, $text_id, $score1, $score2, $score3);
        $stmt->execute();
    }

    public function saveFeedback($title, $subject, $text){
        //feedback table sollte dann auch eine time spalte haben, die automatisch den timestamp erhält
        if (!($stmt = $this->verbindung->prepare("INSERT INTO feedback (title, subject, text) VALUES(?, ?, ?)"))) {
            die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "feedback"));
            return false;
        }
        $stmt->bind_param("sss",$title, $subject, $text);
        $stmt->execute();
        return true;
    }

    public function getText($id) {
        if (!($stmt = $this->verbindung->prepare("SELECT texts.fulltext FROM texts WHERE id=?"))) {
            die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "texts: ".$this->getLastError()));
            return false;
        }

        $stmt->bind_param("s", $id);
        $stmt->execute();
        $stmt->bind_result($res);
        $stmt->fetch();

        return $res;
    }

    public function getTextName($id) {
        if (!($stmt = $this->verbindung->prepare("SELECT texts.name FROM texts WHERE id=?"))) {
            die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "textnames: ".$this->getLastError()));
            return false;
        }

        $stmt->bind_param("s", $id);
        $stmt->execute();
        $stmt->bind_result($res);
        $stmt->fetch();

        return $res;
    }

    public function getAudioByText($text_id) {
        if (!($stmt = $this->verbindung->prepare("SELECT audio.file FROM audio WHERE audio.text_id=?"))) {
            die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "audio: ".$this->getLastError()));
            return false;
        }

        $stmt->bind_param("s", $text_id);
        $stmt->execute();
        $stmt->bind_result($res);
        $stmt->fetch();

        return $res;
    }

    public function getAllDictationsForUser($username, $limit, $offset) {
        $sql = "SELECT r.id as dict_id, t.id as text_id, t.name, r.score, r.correct_words, r.total_words, r.input, r.output FROM results_v0 as r, texts as t WHERE r.text_id = t.id AND r.username='".$username."' ORDER BY r.time_inserted DESC LIMIT ".strval($limit)." OFFSET ".strval($offset);

        $result = $this->query($sql);
        if ($result) {
            return $result;
        } else {
            die($this->errors->createErrorJSON("b_db_couldnt_prepare_sql", "dictation: ".$this->getLastError()));
            return false;
        }
    }

}
