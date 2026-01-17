import requests
import time
import subprocess
from defects4rest.src.utils.shell import run, pretty_section, pretty_step
import json

def issue_29071(args):
    pretty_step("Refresh account_summaries materialized view")
    run([
        "docker", "exec",
        "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        "ActiveRecord::Base.connection.execute('REFRESH MATERIALIZED VIEW account_summaries')"
    ])
    pretty_step("Refresh global_follow_recommendations materialized view")
    run([
        "docker", "exec",
        "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        "ActiveRecord::Base.connection.execute('REFRESH MATERIALIZED VIEW global_follow_recommendations')"
    ])

    pretty_step("Created test user accounts")
    users = ["alice", "bob", "carol"]
    for u in users:
        run([
            "docker", "exec", "mastodon-docker-web-1",
            "bin/tootctl", "accounts", "create", u,
            "--email", f"{u}@localhost", "--confirmed"
        ])

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bin/tootctl", "accounts", "modify", "alice",
        "--role", "Admin"
    ])

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bin/tootctl", "accounts", "modify", "bob",
        "--role", "Moderator"
    ])

    ruby = """
    testadmin = Account.find_by(username: 'testadmin')
    alice = Account.find_by(username: 'alice')
    bob   = Account.find_by(username: 'bob')

    # Create 5 dummy users
    dummy_accounts = []
    5.times do |i|
      username = "user#{i}"

      account = Account.create!(
        username: username,
        domain: nil
      )

      user = User.create!(
        email: "#{username}@localhost",
        password: SecureRandom.hex(16),
        account: account,
        confirmed_at: Time.now,
        current_sign_in_at: Time.now,
        agreement: true
      )

      dummy_accounts << account
    end

    # Have all dummy users follow alice and bob
    dummy_accounts.each do |dummy|
      Follow.create!(account: dummy, target_account: alice)
      Follow.create!(account: dummy, target_account: bob)
    end
    """.strip()

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        ruby
    ])

    ruby = """
    ['alice', 'bob', 'carol'].each do |username|
      account = Account.find_by(username: username)
      raise "Account not found: #{username}" unless account

      # Make them discoverable and unlocked (REQUIRED for suggestions)
      account.update!(
        discoverable: true,
        locked: false
      )

      # Create statuses (REQUIRED for account_summaries view)
      3.times do |i|
        Status.create!(
          account: account,
          text: "Post #{i + 1} from #{username}",
          visibility: 'public',
          language: 'en',
          sensitive: false
        )
      end
    end
    """.strip()

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        ruby
    ])

    ruby = """
    testadmin = Account.find_by(username: 'testadmin')
    alice     = Account.find_by(username: 'alice')
    bob       = Account.find_by(username: 'bob')
    carol     = Account.find_by(username: 'carol')

    [testadmin, alice, bob, carol].compact.each do |account|
      user = account.user
      user&.update!(current_sign_in_at: Time.now)
    end
    """.strip()

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        ruby
    ])

    ruby = """
    ActiveRecord::Base.connection.execute('REFRESH MATERIALIZED VIEW account_summaries')
    ActiveRecord::Base.connection.execute('REFRESH MATERIALIZED VIEW global_follow_recommendations')
    """.strip()

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        ruby
    ])

    run([
        "docker", "exec", "mastodon-docker-db-1",
        "psql", "-U", "mastodon", "-d", "mastodon_production",
        "-c", "SELECT * FROM account_summaries;"
    ])

    run([
        "docker", "exec", "mastodon-docker-db-1",
        "psql", "-U", "mastodon", "-d", "mastodon_production",
        "-c", "SELECT account_id, rank, reason FROM global_follow_recommendations;"
    ])

    ruby = """
    testadmin = Account.find_by(username: 'testadmin')
    bob       = Account.find_by(username: 'bob')

    raise "testadmin not found" unless testadmin
    raise "bob not found" unless bob

    if testadmin.following?(bob)
      testadmin.unfollow!(bob)
    end
    """.strip()

    run([
        "docker", "exec", "mastodon-docker-web-1",
        "bundle", "exec", "rails", "runner",
        ruby
    ])





















