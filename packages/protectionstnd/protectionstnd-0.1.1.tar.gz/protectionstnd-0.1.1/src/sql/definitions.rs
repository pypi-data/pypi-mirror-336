use regex::Regex;

// pip install twine
// twine upload target/wheels/* 

#[derive(Debug)]
pub struct SqlRegexStruct {
    regex_list: Vec<Regex>,
}


impl SqlRegexStruct {
    // Constructor to initialize the struct with a list of regexes
    pub fn new() -> SqlRegexStruct {
        let regexes = vec![
            Regex::new(r"(select)\s.*(from)").unwrap(),      
            Regex::new(r"(insert)\s.*(into)").unwrap(),      
            Regex::new(r"(select)\s.*(case)").unwrap(),      
            Regex::new(r"(delete)\s.*(from)").unwrap(), 
            Regex::new(r"(drop)\s.*(table|function|index|procedure|role|schema|sequence|synonym|trigger|type|view|user)").unwrap(), 
            Regex::new(r"(truncate)\s.*(table|cluster)").unwrap(),
            Regex::new(r"(alter)\s.*(table|user)").unwrap(), 
            Regex::new(r"(update)\s.*(from)").unwrap(), 
            Regex::new(r"(select|merge)\s.*(into)").unwrap(), 
            Regex::new(r"(exec||execute)\s.*(inmediate)").unwrap(), 
            Regex::new(r"(declare)\s.*(begin|end|)").unwrap(),
            Regex::new(r"(begin)\s.*(end)").unwrap(),
            Regex::new(r"sys_context").unwrap(),
            Regex::new(r"(describe|desc|)\s.*(table)").unwrap(),
        ];

        return SqlRegexStruct { regex_list: regexes }
    }

    // Example function to test all regex patterns
    pub fn test_patterns(&self, text: String) -> bool {
        for (_, regex) in self.regex_list.iter().enumerate() {
            // remove comments
            let comment_replacer = Regex::new(r"⁄\*.*?⁄").unwrap();
            let result = comment_replacer.replace_all(&text, "");
            if regex.is_match(&result) {
                return true
            }
        }
        false
    }
}