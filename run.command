#! /usr/bin/env ruby
cd = '~/Documents/DuckBibi/news_analysis'
name = gets.strip
cmd = "cd #{cd} ; python #{name}.py"
system cmd

