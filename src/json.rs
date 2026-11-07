//! Lightweight, zero-dependency, full-featured JSON parser and writer.
//! Supports UTF-8 strings, escapes, numbers, booleans, null, arrays, and objects.

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq)]
pub enum JsonValue {
    Null,
    Bool(bool),
    Number(f64),
    Str(String),
    Array(Vec<JsonValue>),
    Object(BTreeMap<String, JsonValue>),
}

impl JsonValue {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            JsonValue::Str(s) => Some(s.as_str()),
            _ => None,
        }
    }

    pub fn get_str(&self, key: &str, default: &str) -> String {
        self.get(key)
            .and_then(|v| v.as_str())
            .unwrap_or(default)
            .to_string()
    }

    pub fn as_f64(&self) -> Option<f64> {
        match self {
            JsonValue::Number(n) => Some(*n),
            _ => None,
        }
    }

    pub fn get_f64(&self, key: &str, default: f64) -> f64 {
        self.get(key).and_then(|v| v.as_f64()).unwrap_or(default)
    }

    pub fn get_i64(&self, key: &str, default: i64) -> i64 {
        self.get(key)
            .and_then(|v| v.as_f64())
            .map(|n| n.round() as i64)
            .unwrap_or(default)
    }

    pub fn get_u32(&self, key: &str, default: u32) -> u32 {
        self.get(key)
            .and_then(|v| v.as_f64())
            .map(|n| n.max(0.0).round() as u32)
            .unwrap_or(default)
    }

    pub fn get_usize(&self, key: &str, default: usize) -> usize {
        self.get(key)
            .and_then(|v| v.as_f64())
            .map(|n| n.max(0.0).round() as usize)
            .unwrap_or(default)
    }

    pub fn get_bool(&self, key: &str, default: bool) -> bool {
        match self.get(key) {
            Some(JsonValue::Bool(b)) => *b,
            _ => default,
        }
    }

    pub fn get(&self, key: &str) -> Option<&JsonValue> {
        match self {
            JsonValue::Object(map) => map.get(key),
            _ => None,
        }
    }

    pub fn as_array(&self) -> Option<&Vec<JsonValue>> {
        match self {
            JsonValue::Array(arr) => Some(arr),
            _ => None,
        }
    }

    pub fn as_object(&self) -> Option<&BTreeMap<String, JsonValue>> {
        match self {
            JsonValue::Object(map) => Some(map),
            _ => None,
        }
    }

    pub fn to_string_pretty(&self) -> String {
        let mut out = String::new();
        self.write_pretty(&mut out, 0);
        out
    }

    fn write_pretty(&self, out: &mut String, indent: usize) {
        let pad = "  ".repeat(indent);
        let next_pad = "  ".repeat(indent + 1);
        match self {
            JsonValue::Null => out.push_str("null"),
            JsonValue::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
            JsonValue::Number(n) => {
                if n.is_finite() {
                    if (n.fract()).abs() < 1e-9 && n.abs() < 1e15 {
                        out.push_str(&format!("{}", *n as i64));
                    } else {
                        out.push_str(&format!("{}", n));
                    }
                } else {
                    out.push('0');
                }
            }
            JsonValue::Str(s) => {
                out.push('"');
                for ch in s.chars() {
                    match ch {
                        '"' => out.push_str("\\\""),
                        '\\' => out.push_str("\\\\"),
                        '\n' => out.push_str("\\n"),
                        '\r' => out.push_str("\\r"),
                        '\t' => out.push_str("\\t"),
                        c if (c as u32) < 0x20 => {
                            out.push_str(&format!("\\u{:04x}", c as u32));
                        }
                        c => out.push(c),
                    }
                }
                out.push('"');
            }
            JsonValue::Array(items) => {
                if items.is_empty() {
                    out.push_str("[]");
                    return;
                }
                out.push_str("[\n");
                for (i, item) in items.iter().enumerate() {
                    out.push_str(&next_pad);
                    item.write_pretty(out, indent + 1);
                    if i + 1 < items.len() {
                        out.push(',');
                    }
                    out.push('\n');
                }
                out.push_str(&pad);
                out.push(']');
            }
            JsonValue::Object(map) => {
                if map.is_empty() {
                    out.push_str("{}");
                    return;
                }
                out.push_str("{\n");
                let len = map.len();
                for (i, (k, v)) in map.iter().enumerate() {
                    out.push_str(&next_pad);
                    JsonValue::Str(k.clone()).write_pretty(out, indent + 1);
                    out.push_str(": ");
                    v.write_pretty(out, indent + 1);
                    if i + 1 < len {
                        out.push(',');
                    }
                    out.push('\n');
                }
                out.push_str(&pad);
                out.push('}');
            }
        }
    }
}

pub fn parse_json(input: &str) -> Result<JsonValue, String> {
    let chars: Vec<char> = input.chars().collect();
    let mut pos = 0;
    let val = parse_value(&chars, &mut pos)?;
    skip_ws(&chars, &mut pos);
    Ok(val)
}

fn skip_ws(chars: &[char], pos: &mut usize) {
    while *pos < chars.len() {
        let c = chars[*pos];
        if c.is_whitespace() || c == '\u{feff}' {
            *pos += 1;
        } else {
            break;
        }
    }
}

fn parse_value(chars: &[char], pos: &mut usize) -> Result<JsonValue, String> {
    skip_ws(chars, pos);
    if *pos >= chars.len() {
        return Err("Unexpected end of JSON".to_string());
    }
    match chars[*pos] {
        '"' => parse_string(chars, pos).map(JsonValue::Str),
        '{' => parse_object(chars, pos),
        '[' => parse_array(chars, pos),
        't' => {
            if chars[*pos..].starts_with(&['t', 'r', 'u', 'e']) {
                *pos += 4;
                Ok(JsonValue::Bool(true))
            } else {
                Err(format!("Invalid token at {}", *pos))
            }
        }
        'f' => {
            if chars[*pos..].starts_with(&['f', 'a', 'l', 's', 'e']) {
                *pos += 5;
                Ok(JsonValue::Bool(false))
            } else {
                Err(format!("Invalid token at {}", *pos))
            }
        }
        'n' => {
            if chars[*pos..].starts_with(&['n', 'u', 'l', 'l']) {
                *pos += 4;
                Ok(JsonValue::Null)
            } else {
                Err(format!("Invalid token at {}", *pos))
            }
        }
        '-' | '0'..='9' => parse_number(chars, pos),
        c => Err(format!("Unexpected character '{}' at {}", c, *pos)),
    }
}

fn parse_string(chars: &[char], pos: &mut usize) -> Result<String, String> {
    if chars[*pos] != '"' {
        return Err("Expected '\"'".to_string());
    }
    *pos += 1;
    let mut out = String::new();
    while *pos < chars.len() {
        let c = chars[*pos];
        *pos += 1;
        if c == '"' {
            return Ok(out);
        } else if c == '\\' {
            if *pos >= chars.len() {
                return Err("Incomplete escape sequence".to_string());
            }
            let esc = chars[*pos];
            *pos += 1;
            match esc {
                '"' => out.push('"'),
                '\\' => out.push('\\'),
                '/' => out.push('/'),
                'b' => out.push('\u{0008}'),
                'f' => out.push('\u{000c}'),
                'n' => out.push('\n'),
                'r' => out.push('\r'),
                't' => out.push('\t'),
                'u' => {
                    if *pos + 4 > chars.len() {
                        return Err("Incomplete unicode escape".to_string());
                    }
                    let hex: String = chars[*pos..*pos + 4].iter().collect();
                    *pos += 4;
                    let code = u32::from_str_radix(&hex, 16)
                        .map_err(|_| format!("Invalid unicode escape \\u{}", hex))?;
                    if let Some(ch) = char::from_u32(code) {
                        out.push(ch);
                    }
                }
                other => out.push(other),
            }
        } else {
            out.push(c);
        }
    }
    Err("Unterminated string".to_string())
}

fn parse_number(chars: &[char], pos: &mut usize) -> Result<JsonValue, String> {
    let start = *pos;
    while *pos < chars.len() {
        let c = chars[*pos];
        if c.is_ascii_digit() || c == '-' || c == '+' || c == '.' || c == 'e' || c == 'E' {
            *pos += 1;
        } else {
            break;
        }
    }
    let s: String = chars[start..*pos].iter().collect();
    let num: f64 = s
        .parse()
        .map_err(|_| format!("Invalid number '{}' at {}", s, start))?;
    Ok(JsonValue::Number(num))
}

fn parse_array(chars: &[char], pos: &mut usize) -> Result<JsonValue, String> {
    *pos += 1; // skip '['
    let mut arr = Vec::new();
    loop {
        skip_ws(chars, pos);
        if *pos >= chars.len() {
            return Err("Unterminated array".to_string());
        }
        if chars[*pos] == ']' {
            *pos += 1;
            return Ok(JsonValue::Array(arr));
        }
        let val = parse_value(chars, pos)?;
        arr.push(val);
        skip_ws(chars, pos);
        if *pos < chars.len() && chars[*pos] == ',' {
            *pos += 1;
        } else if *pos < chars.len() && chars[*pos] == ']' {
            *pos += 1;
            return Ok(JsonValue::Array(arr));
        } else {
            return Err(format!("Expected ',' or ']' in array at {}", *pos));
        }
    }
}

fn parse_object(chars: &[char], pos: &mut usize) -> Result<JsonValue, String> {
    *pos += 1; // skip '{'
    let mut map = BTreeMap::new();
    loop {
        skip_ws(chars, pos);
        if *pos >= chars.len() {
            return Err("Unterminated object".to_string());
        }
        if chars[*pos] == '}' {
            *pos += 1;
            return Ok(JsonValue::Object(map));
        }
        let key = parse_string(chars, pos)?;
        skip_ws(chars, pos);
        if *pos >= chars.len() || chars[*pos] != ':' {
            return Err(format!("Expected ':' after key '{}' at {}", key, *pos));
        }
        *pos += 1;
        let val = parse_value(chars, pos)?;
        map.insert(key, val);
        skip_ws(chars, pos);
        if *pos < chars.len() && chars[*pos] == ',' {
            *pos += 1;
        } else if *pos < chars.len() && chars[*pos] == '}' {
            *pos += 1;
            return Ok(JsonValue::Object(map));
        } else {
            return Err(format!("Expected ',' or '}}' in object at {}", *pos));
        }
    }
}
