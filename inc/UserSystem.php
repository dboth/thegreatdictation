<?php

require_once __DIR__ . "/config.php";
require_once __DIR__ . "/ErrorHandler.php";
require_once __DIR__ . '/SqlConnector.php';

class UserSystem
{

    public $user_id;

    public function __construct()
    {
        session_start();
        $this->errors = new ErrorHandler(__CLASS__);
        $this->db = new SqlConnector();
    }

    public function setUserInformation($key, $value)
    {
        $_SESSION[$key] = $value;
    }

    public function getUserInformation($key)
    {
        if (isset($_SESSION[$key])) {
            return $_SESSION[$key];
        } else {
            $this->errors->log("b_usersystem_key_not_found", $key);
            return false;
        }
    }

}