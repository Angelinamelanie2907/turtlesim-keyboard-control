import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty


class TurtleKeyboardControl(Node):

    def __init__(self):
        super().__init__('turtle_keyboard_control')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.get_logger().info('Turtle Keyboard Control Started')
        self.get_logger().info('W = Forward')
        self.get_logger().info('S = Backward')
        self.get_logger().info('A = Turn Left')
        self.get_logger().info('D = Turn Right')
        self.get_logger().info('X = Stop')
        self.get_logger().info('Q = Quit')

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.settings
        )
        return key

    def move_turtle(self, key):
        msg = Twist()

        if key == 'w':
            msg.linear.x = 2.0
        elif key == 's':
            msg.linear.x = -2.0
        elif key == 'a':
            msg.angular.z = 2.0
        elif key == 'd':
            msg.angular.z = -2.0
        elif key == 'x':
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        elif key == 'q':
            return False

        self.publisher.publish(msg)
        return True


def main(args=None):
    rclpy.init(args=args)

    node = TurtleKeyboardControl()

    node.settings = termios.tcgetattr(sys.stdin)

    try:
        while rclpy.ok():
            key = node.get_key()

            if not node.move_turtle(key):
                break

            rclpy.spin_once(node, timeout_sec=0.01)

    except KeyboardInterrupt:
        pass

    finally:
        stop_msg = Twist()
        node.publisher.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

