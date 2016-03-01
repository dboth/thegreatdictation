<?php

require_once __DIR__ . "/config.php";
require_once __DIR__ . "/ErrorHandler.php";
require_once __DIR__ . '/SqlConnector.php';

class UserSystem
{
    /* 
        The UserSystem is loaded at the begin of every request and provides session functionality
    */
    public $user_id;
    public static $allowed;

    public function __construct()
    {
        session_start();
        
        //list of the columns in the database and therefore allowed keys
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
        //you cannot set the username this way, and cannot set keys not in the database
        if ($key == "username" || (!in_array($key, self::$allowed)))
            return false;
        
        //set the key for this session
        $_SESSION[$key] = $value;
        
        //if no username is provided do not save the changed information in the db
        if (empty($_SESSION["username"]))
            return true;
        
        //check if user exists in db
        $e = $this->db->query("SELECT null FROM users WHERE username = '".$this->db->esc($_SESSION["username"])."'");
        //if not exists: insert db
        
        if (!$e->num_rows){
            $this->db->query("INSERT INTO users (username, ".$this->db->esc($key).") VALUES ('".$this->db->esc($_SESSION["username"])."','".$this->db->esc($value)."')");
       
        }//else update db
        else
            $this->db->query("UPDATE users SET ".$this->db->esc($key)." = '".$this->db->esc($value)."' WHERE username = '".$this->db->esc($_SESSION["username"])."'");
       
    }

    public function getUserInformation($key = false)
    {
        //if a certain key is specified return that keys value, else return an array of all keys for the user
        if ($key) {
            //the key has to be allowed and set
            if (isset($_SESSION[$key]) && (in_array($key, self::$allowed))) {
                return $_SESSION[$key];
            } else {
                $this->errors->log("b_usersystem_key_not_found", $key);
                return false;
            }
        } else {
            //return all keys
            $out = array();
            foreach (self::$allowed as $key) {
                //do not just return the $_SESSION, in case there will be secret keys later on
                if (isset($_SESSION[$key]))
                    $out[$key] = $_SESSION[$key];
            }
            return $out;
        }
    }
    public function logout(){
         foreach (self::$allowed as $key) {
                //do not just return the $_SESSION, in case there will be secret keys later on
         if (isset($_SESSION[$key]))
                unset($_SESSION[$key]);
         }
        
    }
    public function setUser($username)
    {
        if (!$username)
            return false;
        
        //set the username for the session
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