<?php
class TranslationEngine{
    public function __construct(){
        $this->standardLanguage = $this->getLang();
    }
    
    protected function getLang(){
        //todo: get language by session. if no language is set in the session try to guess via browser data
        return "de-DE";
    }
    
    public function translate($word, $lang = null){
        if ($lang === null){
            $lang = $this->standardLanguage;
        }
        //todo: build translation system. until now only returns the word.
        return $word;
    }
    public function getWords(){
        //todo: crawl through all templates and create a list of words that need to be translated
    }
}