use colored::*;
use std::collections::HashMap;
use std::env;
use std::fs;

// macro_rules! log {
//     ($($arg:tt)*) => ({
//         println!("{}:{}: {}", file!(), line!(), format!($($arg)*));
//     });
// }

fn main() {
    // Check command line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("--Usage: ncnninfo ncnn.param");
        std::process::exit(1);
    }
    // log!("args: {:?}", args);
    let param_content = fs::read_to_string(&args[1]).expect("Error reading param file");

    let param_lines: Vec<&str> = param_content.split('\n').collect();
    // log!("param_lines: {:?}", param_lines);
    let mut counts: HashMap<String, u16> = HashMap::new();

    for line in param_lines.iter().skip(2) {
        let mut words = line.split_whitespace();
        if let Some(word) = words.next() {
            if word == "Input" {
                continue;
            }
            let entry = counts.entry(word.to_string()).or_insert(0);
            *entry += 1;
        }
    }
    // log!("counts: {:?}", counts);
    // 将 HashMap 转换为 Vec<(String, u16)>
    let mut count_vec: Vec<_> = counts.into_iter().collect();

    // 按照 u16 大小进行排序
    // count_vec.sort_by_key(|&(_, count)| count);
    // 按照 u16 大小进行降序排序
    count_vec.sort_by_key(|&(_, count)| std::cmp::Reverse(count));

    // // 打印排序后的结果 -- 打印结束后删除掉，why?
    // for (op_name, count) in count_vec {
    //     println!("Op_name: {}, Count: {}", op_name, count);
    // }

    let layer_data = include_str!("../../go/ncnn_layer.csv");
    let layer_lines: Vec<&str> = layer_data.split('\n').collect();

    let mut dict: HashMap<String, Vec<String>> = HashMap::new();

    for line in layer_lines.iter().skip(1) {
        let cols: Vec<&str> = line.split(',').collect();
        if cols.len() == 7 {
            dict.insert(
                cols[0].to_string(),
                vec![
                    cols[1].to_string(),
                    cols[2].to_string(),
                    cols[3].to_string(),
                    cols[4].to_string(),
                    cols[5].to_string(),
                    cols[6].trim_end_matches('\r').to_string(),
                ],
            );
        }
    }
    // log!("dict: {:?}", dict);

    let plat_os = ["arm", "loongarch", "mips", "riscv", "vulkan", "x86"];
    println!(
        "{:16}{:10}{:10}{:10}{:10}{:10}{:10}{:10}",
        "Op.".green(),
        "Total".green(),
        plat_os[0].green(),
        plat_os[1].green(),
        plat_os[2].green(),
        plat_os[3].green(),
        plat_os[4].green(),
        plat_os[5].green()
    );
    for (op_name, count) in count_vec {
        print!("{:16}{:<10}", op_name.yellow(), count);
        let default_row: Vec<String> = vec!["2", "2", "2", "2", "2", "2"].iter().map(|&s| s.to_string()).collect();
        let row: &Vec<String> = dict.get(&op_name).unwrap_or(&default_row);
        let list: Vec<u8> = row.iter().map(|s| s.parse().unwrap()).collect();
        for &count in list.iter() {
            match count {
                0 => print!("{:10}", ""),
                1 => print!("{:10}", "Y"),
                _ => print!("{:10}", "X".red()),
            }
        }
        println!();
    }
}
