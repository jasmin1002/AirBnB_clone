#!/usr/bin/python3
"""HBNBCommand Class"""
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand subclass Cmd. It uses inherited class
    attribute (prompt) to issue command on each iteration
    through inherited public method cmdloop().

    Arg:
        Cmd (super class): pass down its attributes and methods
        for subclass extends.

    """
    prompt = '(hbnb) '

    __supported_class = ['BaseModel']

    '''=============================================
            Hbnb interpreter commands section
        =========================================='''
    def do_quit(self, line):
        '''Quit command to exit the program'''
        return True

    def do_EOF(self, line):
        '''EOF exit the program and through key strokes: Ctrl + D'''
        return True

    def do_create(self, line):
        '''
        create a new instance of BaseModel
        '''
        line = self.parseline(line)
        class_name = line[0]
        if class_name is None:
            print('** class name missing **')
        elif class_name not in HBNBCommand.__supported_class:
            print('** class doesn\'t exist **')
        else:
            instance_obj = BaseModel()
            instance_obj.save()
            print(instance_obj.id)

    def do_show(self, line):
        '''
        prints the string representation of an instance based on
        class name and id
        '''
        line = self.parseline(line)
        class_name, class_id = line[0], line[1]
        if class_name is None:
            print('** class name missing **')
        elif class_name not in HBNBCommand.__supported_class:
            print('** class doesn\'t exist **')
        elif class_id is None:
            print('** instance id missing **')
        else:
            key = '{}.{}'.format(class_name, class_id)
            try:
                result = storage.all()[key]
                print(result)
            except KeyError:
                print('** no instance found **')
    
    def do_destroy(self, line):
        '''
        deletes an instance based on class name and id
        '''
        line = self.parseline(line)
        class_name, class_id = line[0], line[1]
        if class_name is None:
            print('** class name missing **')
        elif class_name not in HBNBCommand.__supported_class:
            print('** class doesn\'t exist **')
        elif class_id is None:
            print('** instance id missing **')
        else:
            key = '{}.{}'.format(class_name, class_id)
            try:
                storage.destroy(class_name, class_id)
                storage.save()
            except KeyError:
                print('** no instance found **')

    def do_all(self, line):
        '''
        prints all string representation of all instance based or
        or not on the class name
        '''
        line = self.parseline(line)
        class_name = line[0]
        if class_name != None and class_name not in HBNBCommand.__supported_class:
            print('** class doesn\'t exist **')
        else:
            list_all = storage.all()
            if class_name:
                result = [str(list_all[obj]) for obj in list_all if obj.startswith(class_name)]
            else:
                result = [str(list_all[obj]) for obj in list_all]
            print(result)

    def do_update(self, line):
        '''
        updates an instance based on class name and id
        by adding or updating attribute
        '''
        line = line.replace('"', '').strip(' ')
        line = line.split(' ')
        if len(line) == 0:
            print('** class name missing **')
        elif line[0] not in HBNBCommand.__supported_class:
            print('** class doesn\'t exist **')
        elif line[1] is None:
            print('** instance id missing **')
        elif len(line) == 2:
            print('** attribute name missing **')
        elif len(line) == 3:
            print('** value missing **')
        else:
            try:
                storage.update(*line)
                storage.save()
            except KeyError:
                print('** no instance found **')

    '''=============================================
            Overridden base class method section
        =========================================='''
    def emptyline(self):
        '''
        Override emptyline so that Empty line + Enter shouldn't
        execute either of previous cmd(s)
        '''
        return False

    def parseline(self, line):
        '''
        Override super parseline method to parse the agv from
        prompt and pass its result to any calling method.
        '''
        ret = super().parseline(line)
        return ret

    '''================================================
            Overridden docstring section
        ============================================='''
    def help_quit(self):
        print('Quit command to exit the program\n')

    def help_EOF(self):
        print('EOF exit the program\n')

    def help_all(self):
        print('all command fetches and prints all store data\n')

    def help_create(self):
        help_msg = '''
            create command creates a new instance of supported\n
            class name pass as parameter to create command. ex:\n
            create BaseModel\n
            And save the instance to storage file.\n
        '''
        print(help_msg)

    def help_show(self):
        print('Prints the string representation of an instance \
                based on the class name and id\n')

    def help_destroy(self):
        print('Deletes an instance based on the class name and id\n')

    def help_update(self):
        print('Updates an instance based on the class name and id \
                by adding or updating attribute\n')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
