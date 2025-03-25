"""
Data Model Repositories for saving to the Database.
"""

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import or_

from football_data.models import (Base, Player, TeamStaff, TeamLeague, Team, TypeCode,
                                  Position, StatisticCode,
                                  Statistic,
                                  StatisticCategory, Schedule, League)


class BaseRepository:
    """
    Base Repository implementation for Save and Save All.
    """

    maker: sessionmaker

    def __init__(self, maker: sessionmaker):
        """
        Creates a new instance of the Base Repository.
        :param maker: SQL Alchemy Session Maker
        """

        self.maker = maker

    def save(self, model: Base) -> None:
        """
        Saves the model to the database.
        :param model: Base Model Implementation
        :return: None
        """
        session = self.maker()
        try:
            session.begin()
            session.add(model)
            session.commit()
        finally:
            session.close()

    def save_all(self, items: list[Base]) -> None:
        """
        Saves a collection of items to the database.
        :param items: Collection of Base Items.
        :return: None
        """

        session = self.maker()
        try:
            session.begin()
            session.add_all(items)
            session.commit()
        finally:
            session.close()


class PlayerRepository(BaseRepository):
    """
    Repository Implementation for Players.
    """

    def player_exits(self, player: Player) -> bool:
        """
        Validates if a player exists in the database or not.
        :param player: Player
        :return: Bool
        """

        with self.maker() as session:
            result = session.scalars(select(Player).where(Player.url == player.url)).first()
            return result is not None

    def get_player(self, **kwargs) -> Player | None:
        """
        Retrieves a Player by Url.
        :keyword url: Url Value
        :keyword id: ID Value
        :return: Player or None
        """

        conditions = []
        if 'url' in kwargs:
            conditions = [(Player.url == kwargs['url'])]

        if 'id' in kwargs:
            conditions = [(Player.id == int(kwargs['id']))]

        with self.maker() as session:
            return session.scalars(select(Player).where(*conditions)).first()

    def get_players(self, **kwargs) -> list[Player]:
        """
        Retrieves a list of players.
        :keyword position_id: Position ID
        :keyword position_code: Position Code
        :return: List of Players
        """

        position_code = kwargs.get('position_code')
        position_id = kwargs.get('position_id', 0)

        with self.maker() as session:
            if position_code:
                position = session.scalars(
                    select(Position).where(Position.code == position_code)).first()
                if position:
                    position_id = position.id

            if position_id:
                result = session.scalars(
                    select(Player).where(Player.position_id == position_id)).all()
                return result if result else []

            return list(session.scalars(select(Player)).all())


class PositionCodeRepository(BaseRepository):
    """
    Repository for Position Codes.
    """

    def position_code_exists(self, code: Position) -> bool:
        """
        Checks for a Position Code to exist in the system.
        :param code: Position Code
        :return: Bool
        """

        with self.maker() as session:
            result = session.scalars(select(Position).where(Position.code == code.code)).first()
            return result is not None

    def get_position_code(self, **kwargs) -> Position | None:
        """
        Retrieves a Position Code from the system.
        :keyword: id: ID Value
        :keyword: code: Code Value
        :return: Position Code
        """

        conditions = []

        if 'code' in kwargs:
            conditions = [(Position.code == kwargs['code'])]

        if 'id' in kwargs:
            conditions = [(Position.id == int(kwargs['id']))]

        if conditions:
            with self.maker() as session:
                return session.scalars(select(Position).where(*conditions)).first()
        return None

    def get_position_codes(self) -> list[Position]:
        """
        Retrieves the Position Codes.
        :return: List of Position codes
        """

        with self.maker() as session:
            return list(session.scalars(select(Position)).all())


class ScheduleRepository(BaseRepository):
    """
    Repository for working with Schedule information.
    """

    def schedule_exists(self, schedule: Schedule) -> bool:
        """
        Verifies if a schedule entry exists in the database.
        :param schedule: Schedule
        :return: Bool
        """

        with self.maker() as session:
            result = session.scalars(select(Schedule).where(
                Schedule.team_id == schedule.team_id,
                Schedule.opponent_id == schedule.opponent_id,
                Schedule.year_value == schedule.year_value,
                Schedule.week_number == schedule.week_number,
                Schedule.type_id == schedule.type_id)).first()
            return result is not None

    def get_schedule(self, **kwargs) -> Schedule | None:
        """
        Returns the Schedule by id value.
        :keyword id: Schedule ID Value.
        :keyword team id: Team ID
        :keyword game_id: Game ID
        :return: Schedule
        """

        conditions = []
        if 'id' in kwargs:
            conditions.append((Schedule.id == int(kwargs['id'])))
        else:
            if 'team_id' in kwargs and 'game_id' in kwargs:
                conditions = [(Schedule.team_id == int(kwargs['team_id'])),
                              (Schedule.game_id == int(kwargs['game_id']))]

        if conditions:
            with self.maker() as session:
                return session.scalars(select(Schedule).where(*conditions)).first()
        return None

    def get_schedules(self, **kwargs) -> list[Schedule]:
        """
        Retrieves the Schedule Entries for a Team.
        :keyword team_id: Team ID
        :keyword year: Year Value
        :keyword week: Week Number
        :return: List of Schedules
        """
        items = []
        if 'team_id' in kwargs:
            items.append((Schedule.team_id == int(kwargs['team_id'])))
        if 'year' in kwargs:
            items.append((Schedule.year_value == kwargs['year']))
        if 'week' in kwargs:
            items.append((Schedule.week_number == kwargs['week']))

        with self.maker() as session:
            return list(session.scalars(select(Schedule).where(*items)))


class StatisticCategoryRepository(BaseRepository):
    """
    Repository for working with Statistic Category Codes.
    """

    def statistic_category_exists(self, category: StatisticCategory) -> bool:
        """
        Checks if a statistic category code already exists.
        :param category: Statistic Category
        :return: bool
        """
        with self.maker() as session:
            result = session.scalars(
                select(StatisticCategory).where(StatisticCategory.code == category.code)).first()
            return result is not None

    def get_statistic_categories(self) -> list[StatisticCategory]:
        """
        Retrieves the Statistic Category Codes.
        :return: List of Statistic Category codes
        """
        with self.maker() as session:
            return list(session.scalars(select(StatisticCategory)).all())

    def get_statistic_category(self, **kwargs) -> StatisticCategory | None:
        """
        Retrieves the Statistic Category Code by the code value.
        :keyword id: ID Value
        :keyword code: Statistic Category Code
        :return: Statistic Category
        """
        criteria = []
        if 'code' in kwargs:
            criteria = [(StatisticCategory.code == kwargs['code'])]
        if 'id' in kwargs:
            criteria = [(StatisticCategory.id == int(kwargs['id']))]

        if criteria:
            with self.maker() as session:
                return session.scalars(
                    select(StatisticCategory).where(or_(False, *criteria))).first()
        return None


class StatisticRepository(BaseRepository):
    """
    Repository for working with Statistic Entries.
    """

    def statistic_exists(self, stat: Statistic) -> bool:
        """
        Checks if a statistic already exists.
        :param stat: Statistic.
        :return: Bool
        """
        criteria = [
            (Statistic.schedule_id == stat.schedule_id),
            (Statistic.category_id == stat.category_id),
            (Statistic.statistic_code_id == stat.category_id)]

        if stat.player_id:
            criteria.append((Statistic.player_id == stat.player_id))
        if stat.team_id:
            criteria.append((Statistic.team_id == stat.team_id))

        with self.maker() as session:
            result = session.scalars(select(Statistic).where(*criteria)).first()
            return result is not None

    def get_statistics(self, **kwargs) -> list[Statistic]:
        """
        Returns the Statistics from the Database.
        :keyword: player_id Player ID Value
        :keyword: schedule_id Schedule ID Value
        :keyword: team_id Team ID Value
        :return: List of Statistics
        """

        criteria = []
        if 'player_id' in kwargs:
            criteria.append((Statistic.player_id == int(kwargs['player_id'])))
        if 'team_id' in kwargs:
            criteria.append((Statistic.team_id == int(kwargs['team_id'])))
        if 'schedule_id' in kwargs:
            criteria.append((Statistic.schedule_id == int(kwargs['schedule_id'])))

        with self.maker() as session:
            return list(session.scalars(select(Statistic).where(*criteria)).all())

    def get_statistic(self, id_value: int) -> Statistic | None:
        """
        Retrieves a statistic by the ID Value.
        :param id_value: Primary Key ID Value.
        :return: Statistic or None
        """
        with self.maker() as session:
            return session.scalars(select(Statistic).where(Statistic.id == id_value)).first()


class TeamRepository(BaseRepository):
    """
    Repository for interacting with teams.
    """

    def team_exists(self, team: Team) -> bool:
        """
        Checks if a Team exists in the database.
        :param team: Team
        :return: Boolean
        """
        criteria = [
            (Team.code == team.code),
            (Team.url == team.url)
        ]

        with self.maker() as session:
            result = session.scalars(select(Team).where(or_(False, *criteria))).first()
            return result is not None

    def get_teams(self) -> list[Team]:
        """
        Returns a list of teams
        :return: List of Teams
        """
        with self.maker() as session:
            return list(session.scalars(select(Team)).all())

    def get_team(self, **kwargs) -> Team | None:
        """
        Retrieves a Team by Code or ID.
        :keyword id: ID Value
        :keyword code: Team Code
        :keyword url: Team Url
        :keyword name: Team Name
        :return: Team or None
        """

        criteria = []

        if 'code' in kwargs:
            criteria = [(Team.code == kwargs['code'])]
        if 'url' in kwargs:
            criteria = [(Team.url == kwargs['url'])]
        if 'id' in kwargs:
            criteria = [(Team.id == kwargs['id'])]
        if 'name' in kwargs:
            criteria = [(Team.name == kwargs['name'])]

        if criteria:
            with self.maker() as session:
                return session.scalars(select(Team).where(*criteria)).first()
        return None


class TypeCodeRepository(BaseRepository):
    """
    Repository for interacting with Type Codes.
    """

    def type_code_exists(self, code: TypeCode) -> bool:
        """
        Checks if a Type Code already exists.
        :param code: Type Code Value
        :return: boolean
        """
        with self.maker() as session:
            result = session.scalars(select(TypeCode).where(TypeCode.code == code.code)).first()
            return result is not None

    def get_type_code(self, **kwargs) -> TypeCode | None:
        """
        Retrieves a type code from the system.
        :keyword code: Code Value
        :keyword id: ID Value
        :return: Type Code or None
        """

        criteria = []
        if 'id' in kwargs:
            criteria = [(TypeCode.id == kwargs['id'])]
        if 'code' in kwargs:
            criteria = [(TypeCode.code == kwargs['code'])]

        if criteria:
            with self.maker() as session:
                return session.scalars(select(TypeCode).where(or_(False, *criteria))).first()
        return None

    def get_type_codes(self) -> list[TypeCode]:
        """
        Retrieves the Type Codes from the system.
        :return: List of Type Codes
        """
        with self.maker() as session:
            return list(session.scalars(select(TypeCode)).all())


class TeamStaffRepository(BaseRepository):
    """
    Repository for interacting with Team Staff.
    """

    def team_staff_exists(self, staff: TeamStaff) -> bool:
        """
        Validates a team staff entry exists.
        :param staff: Team Staff Entry
        :return: Bool
        """
        conditions = [
            (TeamStaff.team_id == staff.team_id),
            (TeamStaff.player_id == staff.player_id),
            (TeamStaff.year_value == staff.year_value)
        ]
        with self.maker() as session:
            result = session.scalars(select(TeamStaff).where(*conditions)).first()
            return result is not None

    def get_team_staff_entries(self, **kwargs) -> list[TeamStaff]:
        """
        Retrieves Team Staff Entries.
        :keyword team_id: Team ID
        :keyword player_id: Player id value
        :return: List of TeamStaff items.
        """

        conditions = []
        if 'team_id' in kwargs:
            conditions.append((TeamStaff.team_id == int(kwargs['team_id'])))

        if 'player_id' in kwargs:
            conditions.append((TeamStaff.player_id == int(kwargs['player_id'])))

        with self.maker() as session:
            if conditions:
                return list(session.scalars(select(TeamStaff).where(*conditions)).all())
            return list(session.scalars(select(TeamStaff)).all())

    def get_team_staff_entry(self, id_value: int) -> TeamStaff | None:
        """
        Retrieves a Staff Entry by ID value.
        :param id_value: ID Value
        :return: Team Staff of None
        """

        with self.maker() as session:
            return session.scalars(select(TeamStaff).where(TeamStaff.id == id_value)).first()


class LeagueRepository(BaseRepository):
    """
    Repository for interacting with League entries.
    """

    def league_exits(self, league: League) -> bool:
        """
        Validates if a League exists in the Database.
        :param league: League
        :return: Bool
        """
        with self.maker() as session:
            result = session.scalars(select(League).where(League.code == league.code)).first()
            return result is not None

    def get_league(self, **kwargs) -> League | None:
        """
        Retrieves a League from the Database.
        :keyword id: Unique ID Value
        :keyword code: Code value
        :return: League or None
        """

        conditions = []
        if 'id' in kwargs:
            conditions = [(League.id == int(kwargs['id']))]

        if 'code' in kwargs:
            conditions = [(League.code == kwargs['code'])]

        if conditions:
            with self.maker() as session:
                return session.scalars(select(League).where(*conditions)).first()
        return None

    def get_leagues(self) -> list[League]:
        """
        Returns the Leagues in the system
        :return: List of Leagues
        """

        with self.maker() as session:
            return list(session.scalars(select(League)).all())


class TeamLeagueRepository(BaseRepository):
    """
    Repository for interacting with Team League references.
    """

    def team_league_exists(self, team_league: TeamLeague) -> bool:
        """
        Validates Team League entry exists in the Database.
        :param team_league: Team League Entry
        :return: bool
        """

        conditions = [
            (TeamLeague.team_id == team_league.team_id),
            (TeamLeague.league_id == team_league.league_id),
            (TeamLeague.year_value == team_league.year_value)
        ]

        with self.maker() as session:
            result = session.scalars(select(TeamLeague).where(*conditions)).first()
            return result is not None

    def get_team_leagues(self, **kwargs) -> list[TeamLeague]:
        """
        Retrieves a list of Team Leagues from the database.
        :keyword team_id: Team ID
        :keyword league_id: League ID
        :return: List of Team League Entries
        """
        conditions = []
        if 'team_id' in kwargs:
            conditions.append((TeamLeague.team_id == int(kwargs['team_id'])))

        if 'league_id' in kwargs:
            conditions.append((TeamLeague.league_id == int(kwargs['league_id'])))

        with self.maker() as session:
            if conditions:
                return list(session.scalars(select(TeamLeague).where(*conditions)).all())
            return list(session.scalars(select(TeamLeague)).all())

    def get_team_league(self, id_value: int) -> TeamLeague | None:
        """
        Retrieves a Team League Entry from the Database.
        :param id_value: Primary ID Value
        :return: Team League or None
        """
        with self.maker() as session:
            return session.scalars(select(TeamLeague).where(TeamLeague.id == id_value)).first()


class StatisticCodeRepository(BaseRepository):
    """
    Repository for interacting with Statistic Codes.
    """

    def statistic_code_exists(self, code: StatisticCode) -> bool:
        """
        Validates a Statistic Code Exists in the Database.
        :param code: Statistic Code
        :return: bool
        """
        with self.maker() as session:
            result = session.scalars(
                select(StatisticCode).where(StatisticCode.code == code.code)).first()
            return result is not None

    def get_statistic_code(self, **kwargs) -> StatisticCode | None:
        """
        Retrieves a Statistic Code.
        :keyword id: Primary Key ID
        :keyword code: Code Value
        :return: Statistic Code or Noe
        """
        conditions = []
        if 'id' in kwargs:
            conditions = [(StatisticCode.id == int(kwargs['id']))]
        if 'code' in kwargs:
            conditions = [(StatisticCode.code == kwargs['code'])]

        if conditions:
            with self.maker() as session:
                return session.scalars(select(StatisticCode).where(*conditions)).first()
        return None

    def get_statistic_codes(self, **kwargs) -> list[StatisticCode]:
        """
        Retrieves the Statistic Codes.
        :keyword grouping: Code Grouping Value.
        :return: List of Statistic Codes
        """

        if 'grouping' in kwargs:
            stmt = select(StatisticCode).where((StatisticCode.grouping == kwargs['grouping']))
        else:
            stmt = select(StatisticCode)
        with self.maker() as session:
            return list(session.scalars(stmt).all())
