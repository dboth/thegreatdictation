<?php

require_once __DIR__ . "/config.php";
require_once __DIR__ . "/ErrorHandler.php";
require_once __DIR__ . '/SqlConnector.php';

class UserSystem
{

    public $user_id;
    public static $allowed;

    public function __construct()
    {
        session_start();
        self::$allowed = array(
        "username",
        "age",
        "gender",
        "mothertongue",
        "learninglength",
        "livingingerman");
        $this->errors = new ErrorHandler(__CLASS__);
        $this->db = new SqlConnector();
    }

    public function setUserInformation($key, $value)
    {
        if ($key == "username" || (!in_array($key, self::allowed)))
            return false;

        $_SESSION[$key] = $value;
        
        if (empty($_SESSION["username"]))
            return true;
        
        //check if user exists in db
        $e = $this->db->query("SELECT null FROM users WHERE username = '".$this->db->esc($_SESSION["username"])."'");
        //if not exists: insert in db
        if (!$e->num_rows)
            $this->db->query("INSERT INTO users (username, ".$this->db->esc($key).") VALUES ('".$this->db->esc($_SESSION["username"])."','".$this->db->esc($value)."')");
        //else update in db
        else
            $this->db->query("UPDATE users SET ".$this->db->esc($key)." = '".$this->db->esc($value)."' WHERE username = ".$this->db->esc($_SESSION["username"])."'");
        
    }

    public function getUserInformation($key = false)
    {
        if ($key) {
            if (isset($_SESSION[$key]) && (in_array($key, self::allowed))) {
                return $_SESSION[$key];
            } else {
                $this->errors->log("b_usersystem_key_not_found", $key);
                return false;
            }
        } else {
            $out = array();
            foreach (self::$allowed as $key) {
                if (isset($_SESSION[$key]))
                    $out[$key] = $_SESSION[$key];
            }
        }
    }

    public function setUser($username)
    {
        if (!$username)
            return false;
        $_SESSION["username"] = $username;
        
        //select info from database and instatiate
        $e = $this->db->query("SELECT * FROM users WHERE username = '".$this->db->esc($username)."'");
        $r = array();
        if ($e->num_rows)
            $r = $e->fetch_assoc();
        
        foreach (self::$allowed as $key){
            if ($key == "username")
                continue;
            if (!empty($r[$key]))
                $_SESSION[$key] = $r[$key];
            else
                $_SESSION[$key] = "";
        }
        
    }

}