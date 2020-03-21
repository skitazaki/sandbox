require 'spec_helper'

describe service('jupyternb') do
  it { should be_enabled }
  it { should be_running }
end

describe port(8888) do
  it { should be_listening }
end

if os[:family] == 'ubuntu'
  describe file('/etc/init/jupyternb.conf'), :if => os[:release] == '14.04' do
    it { should be_file }
  end
  describe file('/lib/systemd/system/jupyternb.service'), :if => os[:release] == '16.04' do
    it { should be_file }
  end
end

describe file('/opt/jupyternb/environment.yml') do
  it { should be_file }
end

describe file('/opt/jupyternb/jupyter_notebook_config.py') do
  it { should be_file }
end

describe group('jupyternb') do
  it { should exist }
end

describe user('jupyternb') do
  it { should exist }
end

describe file('/opt/jupyternb/notebooks') do
  it { should be_directory }
  it { should be_owned_by 'jupyternb' }
  it { should be_grouped_into 'jupyternb' }
  it { should be_readable.by_user('jupyternb') }
  it { should be_writable.by_user('jupyternb') }
end

describe file('/var/log/jupyternb.log') do
  it { should be_file }
end
