import logging

from src.sql.sql import get_member_data

def memberlist():
    all_member_ids = get_member_data()

    print(all_member_ids)


    # new joined, not in db





    # db_all_ids = [row[0] for row in cursor.fetchall()]


    # for member in guild.members:
    #     if member.id not in db_all_ids:
    #         # Not in DB
    #         cursor.execute("""
    #             INSERT INTO members
    #             (member_id, member_name, account_created, in_server, nickname, joined, is_bot)
    #             VALUES (%s, %s, %s, %s, %s, %s, %s);
    #             """, (member.id, member.name, member.created_at, True, member.display_name, member.joined_at, member.bot))
    #         print(f"Adding member: {member.name} ({member.id})")
