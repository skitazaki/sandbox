require 'spec_helper'

describe package('neo4j') do
  it { should be_installed }
end

describe service('neo4j') do
  it { should be_enabled }
  it { should be_running }
end

unless ENV['TRAVIS']
  [7474, 7687].each do |p|
    describe port(p) do
      it { should be_listening }
    end
  end
end

describe file("/etc/neo4j/neo4j.conf") do 
  it { should be_file }
  its(:content) { should match /dbms.connectors.default_listen_address=0.0.0.0/ }
end

describe user('neo4j') do
  it { should exist }
end

describe group('neo4j') do
  it { should exist }
end
