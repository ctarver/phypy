import numpy as np
import simpy


class MimoTransmitter:
    """ Class that represents an entire MIMO Transmitter Array. Includes channel and precoder."""

    def __init__(self,
                 n_antennas: int = 64,
                 n_users: int = 4,
                 precoder: str = 'zero_forcing',
                 update_precoder_frequency: int = 7):
        self.n_antennas = n_antennas
        self.n_users = n_users
        self.channel_matrix = None  # Will store the channel matrix when we get it.
        self.precoder = ZeroForcing(self.channel_matrix, update_precoder_frequency)

    def update_channel(self, channel):
        """ The channel object exists in its own object. Periodically, our transmitter will get new CSI/channel.
        This method updates the classes copy of the channel"""

    def transmit(self, symbols):
        pass


class LinearPrecoder:
    def __init__(self):
        pass

    def precode(self, symbols):
        out = np.dot(self.precoding_matrix, symbols)
        return out

    def precode_update_process(self, env):
        env.timeout(
            0.001
        )  # Small delay so that we always update based on a new channel
        while True:
            print(f'Current Symbol = {env.now}. Updating precoder')
            self.create_precoder_matrix(self.precoding_matrix)
            yield env.timeout(self.update_rate)


class ZeroForcing(LinearPrecoder):
    def __init__(self, channel_matrix, update_rate):
        self.precoding_matrix = None  # Will be set by create_precoder_matrix method
        self.create_precoder_matrix(channel_matrix)
        self.update_rate = update_rate

    def create_precoder_matrix(self, channel_matrix):
        self.precoding_matrix = channel_matrix


class MIMO_Channel:
    def channel_update_process(self, env):
        while True:
            print(f'Current Symbol = {env.now}. Updating channel')
            self.update_channel()
            yield env.timeout(self.update_rate)


class MimoAwgn(MIMO_Channel):
    def __init__(self, n_users: int = 8, n_antennas: int = 64, n_subcarriers=1200, update_rate: int = 7):
        self.n_users = n_users
        self.n_antennas = n_antennas
        self.n_subcarriers = n_subcarriers
        self.update_rate = update_rate
        self.matrix = 1

    def update_channel(self):
        new_channel = 0.9*old_channel + guassian
        pass


if __name__ == "__main__":
    env = simpy.Environment()
    update_channel_frequency = 1  # Every 2 symbols, make new  MIMO channel
    update_precoder_frequency = 7
    n_users = 4
    n_antennas = 64
    n_subcarriers = 1200
    n_symbols = 64

    channel = MimoAwgn(n_users=n_users, n_antennas=n_antennas, n_subcarriers=n_subcarriers)
    tx = MimoTransmitter(n_users=n_users, n_antennas=n_antennas,
                         update_precoder_frequency=update_precoder_frequency)
    env.process(channel.channel_update_process(env))
    env.process(tx.precoder.precode_update_process(env))
    env.run(until=n_symbols)

    print(tx.n_antennas)
    print(tx.n_users)
    print(tx.precoder)


