require 'spec_helper'

describe package('nginx'), :if => os[:family] == 'redhat' do
  it { should be_installed }
end

describe package('nginx'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe service('nginx'), :if => os[:family] == 'redhat' do
  it { should be_enabled }
  it { should be_running }
end

describe service('nginx'), :if => os[:family] == 'ubuntu' do
  it { should be_enabled }
  it { should be_running }
end

describe port(80) do
  it { should be_listening }
end

describe file('/etc/nginx/nginx.conf') do
  it { should be_file }
  its(:content) { should match /^\s+server_tokens off;$/ }
  its(:content) { should match /^\s+upstream jupyternb_server {$/ }
  its(:content) { should match /^\s+include \/etc\/nginx\/sites-enabled\/\*;$/ }
end

describe file('/etc/nginx/sites-available/default') do
  it { should be_file }
end

describe file('/etc/nginx/sites-enabled/default') do
  it { should_not exist }
end
