<?php
//Template Generator Class

//include translator
require_once __DIR__."/TranslationEngine.php";
require_once __DIR__."/ErrorHandler.php";

class TemplateGenerator{
    public function __construct(){
        //make new translator
        $this->translator = new TranslationEngine();
        //Error Handler
        $this->errors = new ErrorHandler(__CLASS__);
        //pageMarkup contains the webpages html
        $this->pageMarkup = "";

        //get the right page by post or get variables
        $page = $this->getPage();
        //this applies the base template
        $this->applyTemplate($page);
        //apply the page template to the base template
        $this->applyPage($page);
        $this->applyViews();
        $this->applyTranslation();
        $this->applyVars($page);
        $this->applyComponents($page);
    }

    protected function getPage(){
        global $usersystem;
        //first page switcher only works with get.
        switch(@$_GET["p"]){
            //add other pages here. example.org/?p=pagename results in a switch here. "pagename" would be the case.

            case "dictation":
                return array(

                    "vars" => array(
                        "title"=>"The Great Dictation",
                        "header-title" => "Start the Dictation!",
                        "analysispath" => "analysis/index.php",
                        "description" => ""
                        ),
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php",
                        "texts" => "dictation_texts.php"
                    ),
                    "body"=>"dictation.php",
                    "template"=>"default.php"
                );

            case "getstarted":
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"The Great Dictation - Get Started",
                        "header-title"=>"Get Started"
                        ),
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php"
                    ),
                    //the page template (inside frontend/pages)
                    "body"=>"getstarted.html",
                    "template"=>"default.php"
                );

            case "why":
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"The Great Dictation - Why Dictation",
                        "header-title"=>"Why Dictation?"
                        ),
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php"
                    ),
                    //the page template (inside frontend/pages)
                    "body"=>"why.html",
                    "template"=>"default.php"
                );

			case "aboutus":
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"The Great Dictation - About Us",
                        "header-title"=>"About Us"
                        ),
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php"
                    ),
                    //the page template (inside frontend/pages)
                    "body"=>"aboutus.html",
                    "template"=>"default.php"
                );

            case "register":
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"The Great Dictation - Sign In",
                        "header-title"=>"Sign In"
                        ),
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php",
                        "langs" => "language_options.php"
                    ),
                    //the page template (inside frontend/pages)
                    "body"=>"register.html",
                    "template"=>"default.php"
                );

            default:
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"The Great Dictation",
                        "header-title"=>"The Great Dictation"
                        ),
                    //full components can be inserted depending on page name
                    "components" => array(
                        "header-description" => "description.php",
                        "citation" => "citations.php"
                    ),
                    //the page template (inside frontend/pages)
                    "body"=>"home.html",
                    "template"=>"default.php"
                );
        }
    }
    public function printPage(){
        echo $this->pageMarkup;
    }
    protected function applyTemplate($page){
        global $usersystem;
        //applies the base template
        if (file_exists($GLOBALS["conf"]["base_path"]."/frontend/".$page["template"])){
        ob_start();
            require $GLOBALS["conf"]["base_path"]."/frontend/".$page["template"];
        $this->pageMarkup = ob_get_clean();
        } else {
            $this->errors->log("b_page_not_found", $page["template"]);
            return "ERROR: Content couldnt be found";
        }
    }
    protected function applyPage($page){
        global $usersystem;
        //applies the page template
        if (file_exists($GLOBALS["conf"]["base_path"]."/frontend/pages/".$page["body"])){
        ob_start();
            require $GLOBALS["conf"]["base_path"]."/frontend/pages/".$page["body"];
        $page_body = ob_get_clean();
        $this->pageMarkup = str_replace("<tgd_body>",$page_body,$this->pageMarkup);
        } else {
            $this->errors->log("b_page_not_found", $page["body"]);
            return "ERROR: Content couldnt be found";
        }
    }
    protected function applyViews(){
        //replaces every occurence of <tgd_page>page</tgd_page> with the translation of word using the in the constructor specified translators translate method.
        $this->pageMarkup = preg_replace("/<tgd_page>(.*?)<\/tgd_page>/e", '$this->getView("../components/$1")', $this->pageMarkup);
    }
    protected function getView($html){
        if (file_exists($GLOBALS["conf"]["base_path"]."/frontend/pages/".$html)){
        return file_get_contents($GLOBALS["conf"]["base_path"]."/frontend/pages/".$html);} else {
            $this->errors->log("b_view_not_found", $html);
            return "";
        };
    }
    protected function applyTranslation(){
        //replaces every occurence of <tgd_trans>WORD</tgd_trans> with the translation of word using the in the constructor specified translators translate method.
        $this->pageMarkup = preg_replace("/<_>(.*?)<\/_>/e", '$this->translator->translate("$1")', $this->pageMarkup);
    }
    protected function applyVars($page){
        //replace every occurence of <tgd_varname> with the value of vars[varname]
        $from = array_map(array($this,"toVariable"),array_keys($page["vars"]));
        $to = array_values($page["vars"]);
        $this->pageMarkup = str_replace($from,$to,$this->pageMarkup);
        //todo: check if there are unset variables left in the markup
    }
    protected function toVariable($name){
        //varkey to dom varname
        return "<tgd_$name>";
    }

    protected function applyComponents($page){
        $from = array_map(array($this, "toVariable"), array_keys($page["components"]));
        $to = array_map(array($this, 'getComponents'), array_values($page["components"]));
        $this->pageMarkup = str_replace($from, $to, $this->pageMarkup);
    }

    protected function getComponents($path){
        global $usersystem;
        if (file_exists($GLOBALS["conf"]["base_path"]."/frontend/components/".$path)){
            // Opens and runs php file and returns output
            ob_start();
            require $GLOBALS["conf"]["base_path"]."/frontend/components/".$path;
            return ob_get_clean();
        } else {
            $this->errors->log("b_component_not_found", $path);
            return "ERROR: Content couldnt be found";
        }
    }
}
