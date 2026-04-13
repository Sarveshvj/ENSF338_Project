class NavigationHistory:
    #Undo functions works by adding to back of list which
    #will then act as the front of the stack.
    def __init__(self):
        self.back_stack = [] 
        self.current_origin = None
        
        #Not sure if needed
        self.forward_stack = []
    
    def navigate(self, origin, destination):
        if self.current_origin is not None:
            self.back_stack.append(self.current_origin)
        
        if self.forward_stack:
            self.forward_stack = []

        self.current_origin = destination
    
    def undo(self):
        if not self.back_stack:
            print("\nNothing to go back to")
            return self.current_origin
        
        self.forward_stack.append(self.current_origin)
        self.current_origin = self.back_stack.pop()
        return self.current_origin
    
    #Not sure if we need added incase
    def forward(self):
        if not self.forward_stack:
            print("\nNothing to go forward to")
            return self.current_origin

        self.back_stack.append(self.current_origin)
        self.current_origin = self.forward_stack.pop()
        return self.current_origin

#Manual Testing
if __name__ == "__main__":
    nav = NavigationHistory()
    
    nav.navigate("Library", "ICT")
    nav.navigate("ICT", "ENG Block")
    nav.navigate("ENG Block", "Gym")
    print(f"After 3 navigations - Current: {nav.current_origin}, Back: {nav.back_stack}\n")
    
    nav.undo()
    nav.undo()
    print(f"After 2 undos - Current: {nav.current_origin}, Back: {nav.back_stack}, Forward: {nav.forward_stack}\n")
    
    nav.forward()
    print(f"After 1 forward - Current: {nav.current_origin}, Back: {nav.back_stack}, Forward: {nav.forward_stack}\n")
    
    nav.navigate("ENG Block", "Parkade")
    print(f"After new nav - Current: {nav.current_origin}, Back: {nav.back_stack}, Forward: {nav.forward_stack}\n")
    
    nav.undo()
    nav.undo()
    nav.undo()
    nav.undo() 
    
    nav.forward()
    nav.forward()
    nav.forward()
    nav.forward() 