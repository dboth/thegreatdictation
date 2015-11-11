<?php
//Template Generator Class

//include translator
require_once __DIR__."/translationEngine.php";

class TemplateGenerator{
    public function __construct(){
        //make new translator
        $this->translator = new TranslationEngine();
        //pageMarkup contains the webpages html
        $this->pageMarkup = "";
        
        //get the right page by post or get variables
        $page = $this->getPage();
        //this applies the base template
        $this->applyTemplate($page);
        //apply the page template to the base template
        $this->applyPage($page);
        
        $this->applyTranslation();
        $this->applyVars($page);
    }
    
    protected function getPage(){
        //first page switcher only works with get.
        switch(@$_GET["p"]){
            //add other pages here. example.org/?p=pagename results in a switch here. "pagename" would be the case.
            default:
                return array(
                    //inside a template all occurences of <tgd_varname> get replace by the value of vars[varname] in this array. do not use the variables "body" or "trans", as they are reserved.
                    "vars" => array(
                        "title"=>"Testseite",
                        "analysispath"=>"analysis/webconnector.py/analyze"
                        ),
                    //the page template (inside frontend/pages)
                    "body"=>"test.html",
                    "template"=>"template.html"
                );
        }
    }
    public function printPage(){
        echo $this->pageMarkup;
    }
    protected function applyTemplate($page){
        //applies the base template
        $this->pageMarkup = file_get_contents($GLOBALS["base_path"]."/frontend/".$page["template"]);
    }
    protected function applyPage($page){
        //applies the page template
        $page_body = file_get_contents($GLOBALS["base_path"]."/frontend/pages/".$page["body"]);
        $this->pageMarkup = str_replace("<tgd_body>",$page_body,$this->pageMarkup);
    }
    protected function applyTranslation(){
        //replaces every occurence of <tgd_trans>WORD</tgd_trans> with the translation of word using the in the constructor specified translators translate method.
        $this->pageMarkup = preg_replace("/<tgd_trans>(.*?)<\/tgd_trans>/e", '$this->translator->translate("$1")', $this->pageMarkup);
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
}
