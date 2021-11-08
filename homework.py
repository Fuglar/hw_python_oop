class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


coeff_calorie_1 = 18
coeff_calorie_2 = 20


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    coef_time: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM
    pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message
    pass


coeff_calorie_1: int = 18
coeff_calorie_2: int = 20


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration * self.coef_time)


coeff_calorie_3 = 0.035
coeff_calorie_4 = 0.029


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (coeff_calorie_3 * self.weight + (self.get_mean_speed()**2 // self.height) * coeff_calorie_4 * self.weight) * (self.duration * self.coef_time)


coeff_calorie_5 = 1.1
coeff_calorie_6 = 2


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        pass

    def get_distance(self) -> float:
        return (self.length_pool * self.count_pool) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + coeff_calorie_5) * coeff_calorie_6 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    Reader: dict = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}

    if workout_type == 'SWM':
        NewTraining = Reader[workout_type](data[0], data[1], data[2], data[3], data[4])
        return NewTraining
    elif workout_type == 'RUN':
        NewTraining = Reader[workout_type](data[0], data[1], data[2])
        return NewTraining
    elif workout_type == 'WLK':
        NewTraining = Reader[workout_type](data[0], data[1], data[2], data[3])
        return NewTraining
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)