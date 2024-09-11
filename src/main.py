#!/usr/bin python3

import time
from app.commons.dependency_container import DependencyContainer

def main():
    try:    
        
        # Intialize container 
        DependencyContainer.initialize()

        # Run foros workflow
        DependencyContainer.foros_workflow().execute()
        print('executed Foros workflow')

        # waiting 10 minutes to run taks workflow
        time.sleep(50)
            
        # Run taks workflow
        DependencyContainer.tareas_workflow().execute()
        print('executed Tareas workflow')

        return print()
    
    except Exception as e:
        return print(f'There has been an error with the flow execution: {e}')

if __name__ == "__main__":
    
    main()