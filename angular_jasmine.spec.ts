/** 
 * SpyObj creates mock objects with spies for testing purposes 
 *  that mimics the behavior of the actual object
 */
let activeRouterSpy = jasmine.createSpyObj<ActivatedRoute>(['queryParams'])
let routerSpy = jasmine.createSpyObj<Router>(['navigate'])
let webCommunicationServiceSpy = jasmine.createSpyObj<WebserverComunicationService>(['getDocument', 'update_reviewer1', 'update_reviewer2', 'calculate_again'])
let toastrSpy = jasmine.createSpyObj<ToastrService>(['warning', 'success'])
let datepipeSpy = jasmine.createSpyObj<DatePipe>(['transform',])
let translateServiceSpy = jasmine.createSpyObj<TranslateService>(['instant'])


export const createEconomicalMetaData = (
    overrides: Partial<EconomicalMetaData> = {}
  ): EconomicalMetaData => {
    return {
      document_type: 'Type',
      ...overrides,
    };
  };

// Reusable fixtures across multiple test cases within the same test file.
export const createFinding = (overrides: Partial<Finding> = {}): Finding => {
    return {
      value: 'default value',
      ...overrides,
    };
  };

  
export const createCriteria = (overrides: Partial<Criteria> = {}): Criteria => {
    return {
        name: 'default name',
        ...overrides,
    };
};


export const createTrackingMetaData= (
    overrides: Partial<TrackingMetaData> = {}
  ): TrackingMetaData => {
    return {
        created_time: '2023-07-02 14:00:00',
        created_by: "default@user.de",
        ...overrides,
    };
}


describe('WebSinglePageComponent', () => {
    let component: WebSinglePageComponent;
    let document: DocumentSingleElement;
    let activeUser = 'user@posta.de
    let anotherUser = 'user2@posta.de
  
    beforeEach(() => {
      document = {
        id: "12345323233",
        reviewer1: anotherUser,
        reviewer1_time: '2023-06-22 15:27:40',
        reviewer2: activeUser,
        reviewer2_time: '2023-07-12 14:21:04',
        to_update: false
      };
    });
  
    beforeEach(async () => {
      /**
       * Configures the testing module and set up the necessary providers and declarations for component.
       * Creates the component instance with the correct dependencies injected.
       * The first beforeEach block with TestBed.configureTestingModule() ensures
       * that the component's constructor dependencies are properly mocked and injected
       * when the component instance will be created in the second beforeEach-block
       */
      await TestBed.configureTestingModule({
        declarations: [WebSinglePageComponent],
        providers: [
          { provide: ActivatedRoute},
          { provide: Router},
          { provide: WebserverComunicationService},
          { provide: ToastrService},
          { provide: DatePipe},
          { provide: TranslateService}
        ]
      }).compileComponents();
    });
  
    beforeEach(() => {
      /**
       * This block with mock objects customizes the behavior 
       * of those dependencies for individual test cases
       * that were injected in the first BeforeEach-block
       */
      component = new WebSinglePageComponent(activeRouterSpy,
                                             routerSpy,
                                             webCommunicationServiceSpy,
                                             toastrSpy,
                                             datepipeSpy,
                                             translateServiceSpy)
      component.document = document;
      component.document_url = 'https://document.com/';
      component.document_project_id = 39;
    });
  
    // Test cases 
    it('should return the correct document link', () => {
        const link = component.getDocumentLink();
        expect(link).toEqual('https://bla/projects/.../');
      });

    it('should return to_update = false', () => {
        const flag = component.get_update_flag();
        expect(flag).toEqual(false)
    }); 

    it('should set second reviewer', () => {
      // rewritting the created in beforeEach-block attributes 
      // Set up the component and its dependencies
      const documentOneReviewer: DocumentSingleElement = {
        isin: '8888888888',
        reviewer1: activeUser,
        reviewer1_time: '2023-07-17 16:20:00',
        reviewer2: '',
        reviewer2_time: '',
        to_update: true
      };

      component.document = documentOneReviewer
      component.ISIN = '8888888888';
      // Spy on the update_reviewer1 and reviewer2 methods and return a dummy observable
      webCommunicationServiceSpy.update_reviewer2.and.returnValue(of({}));
      spyOn(localStorage, 'getItem').and.returnValue(anotherUser);

      // Pre-test assertions
      expect(component.document.reviewer2).toBe('');
      expect(component.document.reviewer2_time).toBeFalsy();
      
      // Test call
      component.updateReviewers();

      // Check the expected behavior
      expect(webCommunicationServiceSpy.update_reviewer2).toHaveBeenCalledWith(
        '8888888888',
        anotherUser,
        jasmine.any(String) 
      );

      expect(component.document.reviewer2).toBe(anotherUser);
      expect(component.document.reviewer2_time).toBeTruthy();
      expect(webCommunicationServiceSpy.update_reviewer1).not.toHaveBeenCalled;

    });


