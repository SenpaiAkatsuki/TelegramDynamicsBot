# create class with dataclasses
import datetime
from typing import List, Union

from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infrastructure.database.models.groups import GroupSettings, Groups
from infrastructure.database.models.messages import ScheduledMessage, MessageDeliveryStatus, Template


# from tgbot.config import DbConfig


def create_session_pool(db: "DbConfig", echo=False):
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool


class Repo:
    @staticmethod
    async def get_all_groups(session) -> List[Groups]:
        return await session.execute(select(Groups))

    @staticmethod
    async def get_group_by_id(session, group_id: int) -> Groups:
        return await session.execute(select(Groups).where(Groups.group_id == group_id))

    @staticmethod
    async def get_group_id_by_name(session, group_name: str) -> Groups:
        return (await session.execute(select(Groups.group_id).where(Groups.name == group_name))).scalar()

    @staticmethod
    async def create_group(session, group_id: int, group_name: str) -> Groups:
        return await session.execute(
            insert(Groups).values(group_id=group_id, name=group_name).on_conflict_do_nothing()
        )

    @staticmethod
    async def delete_group(session, group_id: int) -> Groups:
        return await session.execute(
            delete(Groups).where(Groups.group_id == group_id)
        )

    @staticmethod
    async def delete_template(session, template_id: int) -> Template:
        return await session.execute(
            delete(Template).where(Template.template_id == template_id)
        )

    @staticmethod
    async def create_scheduled_message(session, send_time: str, next_send_time: datetime.datetime, frequency: str,
                                       group_id: int, status: str, template_id=None,
                                       do_update=True,
                                       ) -> ScheduledMessage:
        scheduled_message = await session.execute(
            select(ScheduledMessage).where(ScheduledMessage.group_id == group_id,
                                           ScheduledMessage.template_id == template_id,
                                           ScheduledMessage.status == 'scheduled'
                                           ).order_by(
                ScheduledMessage.next_send_time.desc()).limit(1)
        )
        scheduled_message = scheduled_message.first()
        if scheduled_message and do_update:
            # Update start time
            return await session.execute(
                update(ScheduledMessage).values(send_time=send_time, next_send_time=next_send_time).where(
                    ScheduledMessage.template_id == template_id, ScheduledMessage.group_id == group_id)
            )

        return await session.execute(
            insert(ScheduledMessage).values(send_time=send_time, frequency=frequency,
                                            template_id=template_id, group_id=group_id, next_send_time=next_send_time,
                                            status=status).on_conflict_do_nothing()
        )

    @staticmethod
    async def update_status_in_scheduled_message_template(session, status: str, scheduled_group_id: int,
                                                          scheduled_template_id) -> ScheduledMessage:
        return await session.execute(
            update(ScheduledMessage).values(status=status).where(
                ScheduledMessage.template_id == scheduled_template_id, ScheduledMessage.group_id == scheduled_group_id)
        )

    @staticmethod
    async def update_time_scheduled_messages(session, next_send_time: datetime.datetime,
                                             group_id: int) -> ScheduledMessage:
        return await session.execute(
            update(ScheduledMessage).values(next_send_time=next_send_time).where(
                ScheduledMessage.group_id == group_id, ScheduledMessage.status == 'scheduled'
            )
        )

    @staticmethod
    async def update_frequency_scheduled_messages(session, frequency: str,
                                                  group_id: int) -> ScheduledMessage:
        return await session.execute(
            update(ScheduledMessage).values(frequency=frequency).where(
                ScheduledMessage.group_id == group_id, ScheduledMessage.status == 'scheduled'
            )
        )

    @staticmethod
    async def update_status_in_scheduled_message_messages(session, status: str,
                                                          scheduled_message_id: int,
                                                          message_link: str = None) -> ScheduledMessage:
        return await session.execute(
            update(ScheduledMessage).values(status=status,
                                            message_link=message_link
                                            ).where(
                ScheduledMessage.scheduled_message_id == scheduled_message_id,
            )
        )

    @staticmethod
    async def update_status_to_all_scheduled_messages(session, status: str) -> ScheduledMessage:
        return await session.execute(
            update(ScheduledMessage).values(status=status).where(ScheduledMessage.status.notin_(['success', 'failed']))
        )

    @staticmethod
    async def create_template(session, name: str, text: str = None, photo=None, caption=None,
                              document=None) -> Template:
        return (
            await session.execute(
                select(Template).from_statement(
                    insert(Template).values(
                        name=name, text=text, photo=photo,
                        caption=caption, document=document
                    ).on_conflict_do_nothing()
                    .returning(Template)
                )
            )
        ).scalars().first()

    @staticmethod
    async def get_all_templates(session) -> List[Template]:
        return (await session.execute(select(Template))).scalars()

    @staticmethod
    async def get_template_by_name(session, name: str) -> Template:
        return (await session.execute(select(Template).where(Template.name == name))).scalars().first()

    @staticmethod
    async def get_all_group_settings(session) -> List[GroupSettings]:
        return await session.execute(select(GroupSettings))

    @staticmethod
    async def create_group_settings(session, group_id: int, frequency: str, start_time: str, end_time: str,
                                    status: str) -> GroupSettings:
        return (
            await session.execute(
                select(GroupSettings).from_statement(
                    insert(GroupSettings).values(group_id=group_id,
                                                 frequency=frequency,
                                                 start_time=start_time,
                                                 end_time=end_time,
                                                 status=status)
                    .on_conflict_do_update(
                        index_elements=[GroupSettings.group_id],
                        set_={
                            "frequency": frequency,
                            "start_time": start_time,
                            "end_time": end_time,
                            "status": status
                        }
                    )
                    .returning(GroupSettings)
                    # TODO if group_id already exists, do update
                )
            )
        ).scalars().first()

    @staticmethod
    async def get_group_settings_by_group_id(session, group_id: int):
        return (
            await session.execute(select(
                GroupSettings.frequency,
                GroupSettings.start_time,
                Groups.name,
                Groups.group_id,
            ).join(
                Groups, Groups.group_id == GroupSettings.group_id
            ).where(GroupSettings.group_id == group_id)))

    @staticmethod
    async def get_all_delivered_messages(session) -> List[MessageDeliveryStatus]:
        return (await session.execute(
            select(MessageDeliveryStatus).where(MessageDeliveryStatus.delivery_status == 'delivered'))).scalars().all()

    @staticmethod
    async def get_scheduled_messages_by_id(session, scheduled_message_id: int) -> ScheduledMessage:
        return await session.execute(
            select(ScheduledMessage).where(ScheduledMessage.scheduled_message_id == scheduled_message_id))

    @staticmethod
    async def get_scheduled_messages_from_template(session, template_id: int) -> ScheduledMessage:
        return (
            await session.execute(
                select(
                    ScheduledMessage.next_send_time,
                    ScheduledMessage.status,
                    Groups.name,
                    ScheduledMessage.message_link,
                    ScheduledMessage.scheduled_message_id
                )
                .join(Groups, Groups.group_id == ScheduledMessage.group_id)
                .where(ScheduledMessage.template_id == template_id)
                .order_by(ScheduledMessage.next_send_time.desc())
                .limit(150)
            )
        )

    @staticmethod
    async def get_templates_ids(session) -> Template:
        return await session.execute(select(Template.template_id))

    @staticmethod
    async def get_template_by_id(session, template_id: int) -> Template:
        return await session.execute(
            select(
                Template.name,
                Template.text,
                Template.photo,
                Template.caption,
                Template.document,
                Template.template_id
            ).where(Template.template_id == template_id)
        )

    @staticmethod
    async def get_all_scheduled_messages_template_ids(session) -> ScheduledMessage:
        return await session.execute(select(ScheduledMessage.template_id).distinct(ScheduledMessage.template_id))

    @staticmethod
    async def update_template(
            session, template_id: int, name: str = None, text: str = None, photo=None, caption=None, document=None
    ) -> Template:
        query = update(Template)
        if name:
            query = query.values(name=name)
        if not text and not caption and not photo and not document:
            raise ValueError('You must provide at least one of the following: text, photo, caption, document')
        query = query.values(text=text)
        query = query.values(photo=photo)
        query = query.values(caption=caption)
        query = query.values(document=document)
        query = query.where(
            Template.template_id == template_id)
        return await session.execute(query)

    @staticmethod
    async def get_all_scheduled_statuses(session):
        return (await session.execute(
            select(ScheduledMessage.status, Template.template_id, Template.name, Groups.name,
                   ScheduledMessage.next_send_time, ScheduledMessage.message_link).
            join(Template, Template.template_id == ScheduledMessage.template_id).
            join(Groups, Groups.group_id == ScheduledMessage.group_id)
            .order_by(ScheduledMessage.next_send_time.desc())
            .limit(150)
        ))

    @staticmethod
    async def get_all_scheduled_messages(session):
        return (await session.execute(
            select(ScheduledMessage, Template, Groups)
            .join(Template, Template.template_id == ScheduledMessage.template_id)
            .join(Groups, Groups.group_id == ScheduledMessage.group_id)
            .where(ScheduledMessage.status == 'scheduled',
                   ScheduledMessage.next_send_time <= datetime.datetime.now()
                   )
        )
                )

    @staticmethod
    async def update_scheduled_message_status(session, scheduled_message_id: int, status: str):
        return (
            await session.execute(
                update(ScheduledMessage).values(status=status).where(
                    ScheduledMessage.scheduled_message_id == scheduled_message_id)
            )
        )
